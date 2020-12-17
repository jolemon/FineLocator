#!/usr/local/bin/python3.7
# Call Dependency
from argparse import ArgumentParser
from graph import Graph
from itertools import permutations
from math_tool import average, sigmoid
import time
import json
from methods_dic import update_id_method_dic
import common


def add_paras_for_method(method_name, paras):
    if not paras:
        return str(method_name) + "()"
    else:
        return str(method_name) + "(" + str(paras) + ")"


def get_cd(udb, parent_dir, filter_file_type = ".java", filter_ref_type = "Call"):
    id_method_dic, method_id_dic, cd_dic = dict(), dict(), dict()

    for file in udb.ents("File"):
        # get abs path
        from_file_name = file.longname(True).lstrip(parent_dir)  # .replace(parent_dir, "").
        if not from_file_name.endswith(filter_file_type):
            continue
        dic = file.depends() if filter_ref_type == "Call" else file.dependsby()
        for ent_key, ref_list in dic.items():
            to_file_name = ent_key.longname(True).lstrip(parent_dir)  # .replace(parent_dir, "")
            for ref in ref_list:
                kind_name = ref.kindname()
                if kind_name != "Call":  # no need to consider "CallBy"
                    continue
                # line_num = ref.line()
                from_ent = ref.scope()
                from_method_name, from_class_name = form_method_name_and_class(from_ent)
                if '(' in from_class_name and ')' in from_class_name:
                    continue

                to_ent = ref.ent()
                to_method_name, to_class_name = form_method_name_and_class(to_ent)
                if '(' in to_class_name and ')' in to_class_name:
                    continue
                # from_signature = from_file_name + '#' + from_class_name + '#' + from_method_name
                # to_signature = to_file_name + '#' + to_class_name + '#' + to_method_name
                from_signature = '{}{}{}{}{}'.format(from_file_name, common.path_class_splitor,
                                                     from_class_name, common.class_sig_splitor, from_method_name)
                to_signature = '{}{}{}{}{}'.format(to_file_name, common.path_class_splitor,
                                                   to_class_name, common.class_sig_splitor, to_method_name)

                from_id = update_id_method_dic(id_method_dic = id_method_dic, method_id_dic = method_id_dic,
                                               method = from_signature)
                to_id = update_id_method_dic(id_method_dic = id_method_dic, method_id_dic = method_id_dic,
                                             method = to_signature)

                if filter_ref_type == "Call":
                    dic_key, dic_value = from_id, to_id
                    add_to_dic(cd_dic, dic_key, dic_value)
                else:
                    dic_key, dic_value = to_id, from_id
                    add_to_dic(cd_dic, dic_key, dic_value)

    return id_method_dic, cd_dic


def form_method_name_and_class(ent):
    ent_name_parts = ent.name().split('.')
    class_name, class_method = ent_name_parts[0], ent_name_parts[1]
    method_simple_name = str(ent.simplename())
    # 构造器作特殊处理: 在这里构造器ent与一般方法的ent不一样, 指向的是类实体而非方法实体，没有paras，因此得不到构造器方法的参数，所以不考虑构造器

    # if 'class_name' is a package name
    if class_name.islower():
        return '()', '()'

    method_paras = ent.parameters()
    method_name = add_paras_for_method(method_name = method_simple_name, paras = method_paras)
    method_type = ent.type()
    if method_type:
        method_name = '{} {}'.format(method_type, method_name)
    return method_name, class_name


def add_to_dic(dic, key, value):
    if key not in dic:
        dic[key] = [value]
    else:
        if value not in dic[key]:
            dic[key].append(value)


def build_graph(dic):
    return Graph(dic)


def build_cd_dic(graph, id_method_dic, save_path):
    vertices = graph.vertices()
    print("Calculate path for methods of size : %d" % len(vertices))
    cd_length_dic, sigmoid_cd_dic = dict(), dict()
    vertices_permutations = permutations(vertices, 2)
    for cd_pair in vertices_permutations:
        start_vertice, end_vertice = cd_pair[0], cd_pair[1]
        path = graph.find_shortest_path(start = start_vertice, end = end_vertice)
        if path:
            cd_length_dic[cd_pair] = len(path)
    avg_shortest_length = average(cd_length_dic.values())

    for cd_pair in cd_length_dic:
        key = '{}{}{}'.format(cd_pair[0], common.ss_key_splitor, cd_pair[1])
        sigmoid_cd_dic[key] = sigmoid(1.0 - cd_length_dic[cd_pair] / avg_shortest_length)

    print("Call dictionary size: %d" % len(sigmoid_cd_dic))
    with open(save_path, 'w') as save_file:
        save_file.write(json.dumps(sigmoid_cd_dic))
    with open('{}.dic'.format(save_path), 'w') as dic_file:
        dic_file.write(json.dumps(id_method_dic))
    return


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-u", "--udb_path",   dest = "udb_path",   required = True)
    parser.add_argument("-s", "--save_path",  dest = "save_path",  required = True)
    parser.add_argument("-p", "--parent_dir", dest = "parent_dir", required = True)
    parser.add_argument("-a", "--api_path",   dest = "api_path",   required = True)
    args = parser.parse_args()
    udb_path = args.udb_path
    save_path = args.save_path
    parent_dir = args.parent_dir
    api_path = args.api_path

    import sys
    sys.path.append(api_path)  # api_path: /Applications/Understand.app/Contents/MacOS/Python

    import understand as us
    start = time.process_time()
    print("Start Calculate Call Dependency...")
    db = us.open(udb_path)
    id_method_dic, cd_dic = get_cd(udb = db, parent_dir = parent_dir)
    db.close()
    cd_graph = build_graph(cd_dic)
    build_cd_dic(graph = cd_graph, id_method_dic = id_method_dic, save_path = save_path)
    elapsed = round(time.process_time() - start, 2)
    print("Finished Calculate Call Dependency. Time used : %.2f seconds" % elapsed)
