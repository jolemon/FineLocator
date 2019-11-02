from argparse import ArgumentParser
import json
import time
from handle_cd_method import trim_method
import os
from math_tool import average
from ss import load_cv
import numpy as np

alpha = 0.8
beta = 0.1
gamma = 0.1


def find_v_by_sharp_k(key, dic, flag = True):
    if key in dic:
        return dic[key]
    else:
        parts = key.split('分')
        m0 = parts[0]
        m1 = parts[1]
        switch_key = m1 + '分' + m0
        if switch_key in dic:
            return dic[switch_key]
        else:
            if flag is True:
                # step 1 : remove "@* " and function modifier and "throws *"
                trim_m0 = trim_method(m0)
                trim_m1 = trim_method(m1)
                # step 2 : try to find new key in dic again
                new_key = trim_m0 + '分' + trim_m1
                return find_v_by_sharp_k(new_key, dic, flag = False)
            else:
                return None


def calculate_ac(ss_path, tp_path, cd_path):
    ac_dic = dict()
    with open(ss_path, 'r') as ss_file:
        ss_dic = json.loads(ss_file.read())
    with open(tp_path, 'r') as tp_file:
        tp_dic = json.loads(tp_file.read())
    with open(cd_path, 'r') as cd_file:
        cd_dic = json.loads(cd_file.read())

    print("load ss, tp, cd dictionary ready.")
    for tp_key in tp_dic:
        tp_value = tp_dic[tp_key]
        ss_value = find_v_by_sharp_k(tp_key, ss_dic)
        if ss_value is None:
            continue
        cd_value = find_v_by_sharp_k(tp_key, cd_dic)
        if cd_value is None:
            cd_value = 0

        ac_value = alpha * ss_value + beta * tp_value + gamma * cd_value
        ac_dic[tp_key] = ac_value

    del ss_dic, tp_dic, cd_dic
    print("ac size:", len(ac_dic))
    avglist = ac_dic.values()
    avg_ac = average(avglist, len(avglist))
    print("average augmentation coefficient is", avg_ac)

    # before method augmentation, filter ac that is lower than avg_ac.
    for ac_key in ac_dic:
        if ac_dic[ac_key] < avg_ac:
            del ac_dic[ac_key]
    return ac_dic


def method_augmentation(cv_path, ac_dic, save_path):
    methods_dic = load_cv(cv_path)
    for ac_key in methods_dic:
        ac_key.split()
    for method in methods_dic:
        doc_vector = methods_dic[method]
        for ac_key in ac_dic:
            if method in ac_key:
                another_method = ac_key.replace(method, "").replace("#", "")
                print(another_method)
                try:
                    another_doc = methods_dic[another_method]
                except KeyError:
                    print(another_method, "not found in methods dic.")
                    continue

                doc_vector = doc_vector + another_doc * ac_dic[ac_key]
                methods_dic[method] = doc_vector
    with open(save_path, 'w') as save_file:
        save_file.write(json.dumps(methods_dic))
    return




if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-ss", "--ss_path", dest = "ss_path", required = True)
    parser.add_argument("-tp", "--tp_path", dest = "tp_path", required = True)
    parser.add_argument("-cd", "--cd_path", dest = "cd_path", required = True)
    parser.add_argument("-c",  "--code_vector_dir", dest = "code_vector_dir", required = True)
    parser.add_argument("-s", "--save_path", dest = "save_path", required = True)

    args = parser.parse_args()
    ss_path = args.ss_path
    tp_path = args.tp_path
    cd_path = args.cd_path
    code_vector_dir = args.code_vector_dir
    save_path = args.save_path

    start = time.process_time()
    print("Finally, Start to Calculate Query Expansion...")
    ac_dic = calculate_ac(ss_path = ss_path, tp_path = tp_path, cd_path = cd_path)
    # method_augmentation(cv_path = code_vector_dir, ac_dic = ac_dic, save_path = save_path)

    elapsed = round(time.process_time() - start, 2)
    print("Finished Calculate Query Expansion. Time used : ", elapsed, "s.")
    print("File size is around : ", str(round(os.path.getsize(save_path) / (1024 * 1024 * 1024), 2)), "G.")