from argparse import ArgumentParser
import json
import time
from handle_cd_method import trim_method
import os
from math_tool import average
from ss import load_cv
from itertools import combinations

alpha = 0.8
beta = 0.1
gamma = 0.1


def find_v_by_sharp_k(sharp_key_pair, key_id_dic, cd_dic, cd_sig2id_dic):
    parts = sharp_key_pair.split('分')
    m0 = parts[0]
    m1 = parts[1]
    m0_sig = key_id_dic[m0]
    m1_sig = key_id_dic[m1]

    # step 1 : remove "@* " and function modifier and "throws *"
    trim_m0 = trim_method(m0_sig)
    trim_m1 = trim_method(m1_sig)

    # step 2 : try to find new key in dic again

    if trim_m0 in cd_sig2id_dic and trim_m1 in cd_sig2id_dic:
        m0_id = cd_sig2id_dic[trim_m0]
        m1_id = cd_sig2id_dic[trim_m1]

        key = m0_id + '分' + m1_id
        if key in cd_dic:
            return cd_dic[key]
        else:
            switch_key = m1_id + '分' + m0_id
            if switch_key in cd_dic:
                return cd_dic[switch_key]
            else:
                return None
    else:
        return None


def calculate_ac(ss_path, tp_path, cd_path, save_path):
    ac_dic = dict()
    with open(ss_path, 'r') as ss_file, open(ss_path + '.dic', 'r') as ss_id_file:
        ss_dic = json.loads(ss_file.read())
        # ss_id_dic = json.loads(ss_id_file.read())
    with open(tp_path, 'r') as tp_file, open(tp_path + '.dic', 'r') as tp_id_file:
        tp_dic = json.loads(tp_file.read())
        tp_id_dic = json.loads(tp_id_file.read())
    with open(cd_path, 'r') as cd_file, open(cd_path + '.dic', 'r') as cd_id_file:
        cd_dic = json.loads(cd_file.read())
        cd_id2sig_dic = json.loads(cd_id_file.read())

    # convert dict
    cd_sig2id_dic = dict(zip(cd_id2sig_dic.values(), cd_id2sig_dic.keys()))

    print("load ss, tp, cd dictionary ready.")
    for tp_key in tp_dic:
        tp_value = tp_dic[tp_key]

        if tp_key in ss_dic:
            ss_value = ss_dic[tp_key]
        else:
            print(tp_key, 'not in ss_dic')
            continue

        cd_value = find_v_by_sharp_k(tp_key, tp_id_dic, cd_dic, cd_sig2id_dic = cd_sig2id_dic)
        if cd_value is None:
            cd_value = 0

        ac_value = alpha * ss_value + beta * tp_value + gamma * cd_value
        ac_dic[tp_key] = ac_value

    print("ac size:", len(ac_dic))

    sum = 0
    for value in ac_dic.values():
        sum += value
    avg_ac = float(sum / len(ac_dic))
    print("average augmentation coefficient is", avg_ac)

    # before method augmentation, filter ac that is lower than avg_ac.
    # list(ac_dic.keys()) 另存一个变量，重新申请内存空间
    for ac_key in list(ac_dic.keys()):
        if ac_dic[ac_key] < avg_ac:
            del ac_dic[ac_key]

    # del ss_dic, tp_dic, cd_dic
    with open(save_path + ".acdic", 'w') as save_file:
        save_file.write(json.dumps(ac_dic))
    return ac_dic




def method_augmentation(cv_path, ac_dic, save_path):
    id_method_dic, id_value_dic = load_cv(cv_path)

    result_dic = dict()

    for ac_key in ac_dic:
        ids = ac_key.split("分")
        ac_value = ac_dic[ac_key]
        id1 = int(ids[0])
        id2 = int(ids[1])

        doc_vector1 = id_value_dic[id1]
        doc_vector2 = id_value_dic[id2]

        if id1 not in result_dic:
            result_dic[id1] = doc_vector1 + doc_vector2 * ac_value
        else:
            result_dic[id1] += doc_vector2 * ac_value

        if id2 not in result_dic:
            result_dic[id2] = doc_vector2 + doc_vector1 * ac_value
        else:
            result_dic[id2] += doc_vector1 * ac_value

        # print(result_dic[id1])
        # print(result_dic[id2])

    with open(save_path, 'w') as save_file:
        save_file.write(json.dumps(result_dic))

    return





def load_ac_dic(path):
    with open(path + ".acdic", 'r') as f:
        dic = json.loads(f.read())
    return dic

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
    # ac_dic = calculate_ac(ss_path = ss_path, tp_path = tp_path, cd_path = cd_path, save_path = save_path)
    ac_dic = load_ac_dic(path = save_path)
    method_augmentation(cv_path = code_vector_dir, ac_dic = ac_dic, save_path = save_path)

    elapsed = round(time.process_time() - start, 2)
    print("Finished Calculate Query Expansion. Time used : ", elapsed, "s.")
    print("File size is around : ", str(round(os.path.getsize(save_path) / (1024 * 1024 * 1024), 2)), "G.")