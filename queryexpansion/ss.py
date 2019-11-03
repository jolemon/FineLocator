# Semantic similarity
import numpy as np
import os
from argparse import ArgumentParser
from itertools import combinations
import time
from math_tool import cosine_similarity
import json
from methods_dic import build_methods_dic

# delete blank space, "[[    " from head and "]]" from tail
def trim_text(string):
    return string.strip().replace("[[", "").replace("]]", "").strip()


# read one line from br file and parse this line to a vector in shape of (1, dim)
def load_brv(file_path, dim):
    with open(file_path, 'r') as f:
        vec_text = f.readline()
        trim_vec_text = trim_text(vec_text)
        arr = np.fromstring(string = trim_vec_text, sep = ',    ')
        vec = arr.reshape((-1, dim), order = 'C')
        return vec


def _load_single_cv(id_method_dic, id_value_dic, abs_file_path, dim, parent_dir):
    with open(abs_file_path, 'r') as f:
        lines = f.readlines()
        for k in range(0, len(lines)-1, 2):
            signature = lines[k+1]
            signature = signature.strip().replace("分", "")
            # remove parent_dir because the path is different with tp_dir and cd_dir.
            # There is already a "#" ahead of signature in file,
            # so don't need to append another "#"
            relative_path = abs_file_path.replace(parent_dir, "")
            signature = relative_path + signature
            vec_text = lines[k]
            trim_vec_text = trim_text(vec_text)
            arr = np.fromstring(string = trim_vec_text, sep = ',    ')
            vec = arr.reshape((-1, dim), order = 'C')

            build_methods_dic(signature, vec, id_method_dic, id_value_dic)
    return


def load_cv(dir_path, dim = 300):
    id_method_dic = dict()
    id_value_dic = dict()
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                _load_single_cv(id_method_dic = id_method_dic, id_value_dic = id_value_dic,
                                abs_file_path = file_path, dim = dim, parent_dir = dir_path)

    return id_method_dic, id_value_dic


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-c" , "--code_vector_dir", dest = "code_vector_dir", required = True)
    parser.add_argument("-br", "--br_vector_path" , dest = "br_vector_path" , required = True)
    parser.add_argument("-d" , "--dim"            , dest = "dim"            , required = True)
    parser.add_argument("-s" , "--save_path"      , dest = "save_path"      , required = True)

    args = parser.parse_args()
    code_vector_dir = args.code_vector_dir
    br_vector_path  = args.br_vector_path
    dim = int(args.dim)
    save_path = args.save_path

    # br Vec
    br_vec = load_brv(file_path = br_vector_path, dim = dim)

    id_method_dic, id_value_dic = load_cv(dir_path = code_vector_dir, dim = dim)

    keys = id_method_dic.keys()
    print("Calculate methods of size :", str(len(keys)))
    comb_list = list(combinations(keys, 2))
    start = time.process_time()
    print("Start Calculate Semantic Similarity...")
    ss_dic = dict()
    for ss in comb_list:
        m1 = ss[0]
        m2 = ss[1]
        vec1 = id_value_dic[m1]
        vec2 = id_value_dic[m2]
        cs = cosine_similarity(vec1 = vec1, vec2 = vec2)
        ss_dic[str(m1)+"分"+str(m2)] = cs

    with open(save_path, 'w') as save_file:
        save_file.write(json.dumps(ss_dic))

    with open(save_path+".dic", 'w') as dic_file:
        dic_file.write(json.dumps(id_method_dic))
    elapsed = round(time.process_time() - start, 2)
    print("Finished Calculate Semantic Similarity. Time used : ", elapsed, "s.")
    print("File size is around : ", str(round(os.path.getsize(save_path) / (1024 * 1024 ), 2)), "M.")