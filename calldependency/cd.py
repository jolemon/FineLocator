#!/usr/local/bin/python3.7
import sys
sys.path.append('/Applications/Understand.app/Contents/MacOS/Python')
import understand as us
from argparse import ArgumentParser
from graph import Graph
from itertools import permutations


def add_paras_for_method(method_name, paras):
    if paras is None:
        return str(method_name) + "()"
    else:
        return str(method_name) + "(" + str(paras) + ")"


def get_cd(udb, save_path, filter_file_type = ".java", filter_ref_type = "Call"):
    save_file = open(save_path, 'w')

    cd_dic = {}

    for f in udb.ents("File"):
        from_file_name = f.longname(True) # get abs path
        if not str(from_file_name).endswith(filter_file_type):
            continue

        # print("filename : " + fromFileName)
        if filter_ref_type == "Call":
            dic = f.depends()
        else:
            dic = f.dependsby()

        for entKey in dic:
            ref_list = dic[entKey]
            to_file_name = entKey.longname(True)  # get abs path
            for ref in ref_list:
                kindname = ref.kindname()
                if kindname == "Call":   # no matter "Call" or "Callby"
                    line_num = ref.line()

                    from_ent = ref.scope()
                    from_method_paras = from_ent.parameters()
                    from_method_name = add_paras_for_method(method_name = from_ent.simplename(), paras = from_method_paras)

                    to_ent = ref.ent()
                    to_method_paras = to_ent.parameters()
                    to_method_name = add_paras_for_method(method_name = to_ent.simplename(), paras = to_method_paras)
                    if filter_ref_type == "Call":
                        # line = from_file_name + '内' + from_method_name + '调用' + to_file_name + '内' + to_method_name + '行' + str(line_num)
                        # save_file.write(line+'\n')
                        dic_key   = from_file_name + '#' + from_method_name
                        dic_value = to_file_name   + '#' + to_method_name
                        add_to_dic(cd_dic, dic_key, dic_value)
                    else:
                        # line = from_file_name + '内' + from_method_name + '被调' + to_file_name + '内' + to_method_name + '行' + str(line_num)
                        # save_file.write(line + '\n')
                        dic_key   = to_file_name   + '#' + to_method_name
                        dic_value = from_file_name + '#' + from_method_name
                        add_to_dic(cd_dic, dic_key, dic_value)

    save_file.write(str(cd_dic))
    save_file.close()
    return cd_dic


def add_to_dic(dic, key, value):
    if key not in dic:
        dic[key] = [value]
    else:
        if value not in dic[key]:
            dic[key].append(value)
        # else:
        #     print(key + " , " + value)


def build_graph(dic):
    return Graph(dic)


def build_cd_matrix(graph):
    vertices = graph.vertices()
    permutations_list = list(permutations(vertices, 2))
    for tp in permutations_list:
        start_vertice = tp[0]
        end_vertice = tp[1]
        path = graph.find_shortest_path(start = start_vertice, end = end_vertice)
        if path is not None:
            print(path)
            print(len(path))

    return


if __name__ == "__main__":
    # parser = ArgumentParser()
    # parser.add_argument("-u", "--udb_path", dest = "udb_path", required = True)
    # parser.add_argument("-s", "--save_path", dest = "save_path", required = True)
    # args = parser.parse_args()
    # udb_path = args.udb_path
    # save_path = args.save_path
    # db = us.open(udb_path)
    # cd_dic = get_cd(udb = db, filter_ref_type = "Call", save_path = save_path)   # or filter_ref_type = "Callby")
    # db.close()
    # build_graph(cd_dic)

    dub = us.open("/Users/lienming/Time_3/Time_3.udb")
    cd_dic = get_cd(dub, save_path = "/Users/lienming/FineLocator/expRes/cd/Time/Time_3")
    cd_graph = build_graph(cd_dic)
    build_cd_matrix(graph = cd_graph)