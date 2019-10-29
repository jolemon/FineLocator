#!/usr/local/bin/python3.7

# Call Dependency

import sys
sys.path.append('/Applications/Understand.app/Contents/MacOS/Python')
import understand as us
from argparse import ArgumentParser
from graph import Graph
from itertools import permutations
from math_tool import average, sigmoid
import time
import json
import os

def add_paras_for_method(method_name, paras):
    if paras is None:
        return str(method_name) + "()"
    else:
        return str(method_name) + "(" + str(paras) + ")"


def get_cd(udb, parent_dir, filter_file_type = ".java", filter_ref_type = "Call"):
    # save_file = open(save_path, 'w')

    cd_dic = {}

    for f in udb.ents("File"):
        from_file_name = f.longname(True).replace(parent_dir, "") # get abs path
        if not str(from_file_name).endswith(filter_file_type):
            continue

        # print("filename : " + fromFileName)
        if filter_ref_type == "Call":
            dic = f.depends()
        else:
            dic = f.dependsby()

        for entKey in dic:
            ref_list = dic[entKey]
            to_file_name = entKey.longname(True).replace(parent_dir, "")  # get abs path
            for ref in ref_list:
                kindname = ref.kindname()
                if kindname == "Call":   # no matter "Call" or "Callby"
                    # line_num = ref.line()

                    from_ent = ref.scope()
                    # print()

                    from_method_paras = from_ent.parameters()
                    from_method_name = add_paras_for_method(method_name = from_ent.simplename(), paras = from_method_paras)
                    from_method_type = from_ent.type()
                    if from_method_type is not None:
                        from_method_name = from_method_type + ' ' + from_method_name

                    to_ent = ref.ent()
                    to_method_paras = to_ent.parameters()
                    to_method_name = add_paras_for_method(method_name = to_ent.simplename(), paras = to_method_paras)
                    to_method_type = to_ent.type()
                    if to_method_type is not None:
                        to_method_name = to_method_type + ' ' + to_method_name
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

    # save_file.write(str(cd_dic))
    # save_file.close()
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


def build_cd_dic(graph, save_path):
    save_file = open(save_path, 'w')
    vertices = graph.vertices()
    permutations_list = list(permutations(vertices, 2))
    cd_dic = dict()
    sigmoid_cd_dic = dict()
    length_list = []
    for cd_pair in permutations_list:
        start_vertice = cd_pair[0]
        end_vertice   = cd_pair[1]
        path = graph.find_shortest_path(start = start_vertice, end = end_vertice)
        if path is not None:
            path_length = len(path)
            cd_dic[cd_pair] = path_length
            length_list.append(path_length)
        else:
            sigmoid_cd_dic[start_vertice+'分'+end_vertice] = 0

    size = len(length_list)
    avg_shortest_length = average(length_list, size)
    for cd_pair in cd_dic:
        sigmoid_cd_dic[cd_pair[0]+'分'+cd_pair[1]] = sigmoid(1 - cd_dic[cd_pair] / avg_shortest_length)
        # print(cd_pair)
        # print(sigmoid_cd_dic[cd_pair])

    save_file.write(json.dumps(sigmoid_cd_dic))
    save_file.close()
    return


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-u", "--udb_path",   dest = "udb_path",   required = True)
    parser.add_argument("-s", "--save_path",  dest = "save_path",  required = True)
    parser.add_argument("-p", "--parent_dir", dest = "parent_dir", required = True)
    args = parser.parse_args()
    udb_path = args.udb_path
    save_path = args.save_path
    parent_dir = args.parent_dir

    start = time.process_time()
    print("Start Calculate Call Dependency...")
    db = us.open(udb_path)
    cd_dic = get_cd(udb = db, parent_dir = parent_dir)
    db.close()
    cd_graph = build_graph(cd_dic)
    build_cd_dic(graph = cd_graph, save_path = save_path)
    elapsed = round(time.process_time() - start, 2)
    print("Finished Calculate Call Dependency. Time used : ", elapsed, "s.")
    print("File size is around : ", str(round(os.path.getsize(save_path) / (1024 * 1024 * 1024), 2)), "G.")
    # dub = us.open("/Users/lienming/Time_3/Time_3.udb")
    # cd_dic = get_cd(dub)
    # cd_graph = build_graph(cd_dic)
    # build_cd_dic(graph = cd_graph, save_path = "/Users/lienming/FineLocator/expRes/cd/Time/Time_3")