# Semantic similarity
import numpy as np
import os
from argparse import ArgumentParser
from itertools import combinations
import time
from math_tool import cosine_similarity
import json

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


def _load_single_cv(abs_file_path, dim, parent_dir):
    dic = dict()
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

            dic[signature] = vec
        return dic


def load_cv(dir_path):
    methods_dic = dict()
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                sub_dic = _load_single_cv(abs_file_path = file_path, dim = dim, parent_dir = dir_path)
                methods_dic.update(sub_dic)
    return methods_dic


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


    methods_dic = load_cv(dir_path = code_vector_dir)
    comb_list = list(combinations(methods_dic.keys(), 2))
    start = time.process_time()
    print("Start Calculate Semantic Similarity...")
    ss_dic = dict()
    for ss in comb_list:
        m1 = ss[0]
        m2 = ss[1]
        vec1 = methods_dic[m1]
        vec2 = methods_dic[m2]
        cs = cosine_similarity(vec1 = vec1, vec2 = vec2)
        ss_dic[m1+"分"+m2] = cs

    with open(save_path, 'w') as save_file:
        save_file.write(json.dumps(ss_dic))
    elapsed = round(time.process_time() - start, 2)
    print("Finished Calculate Semantic Similarity. Time used : ", elapsed, "s.")
    print("File size is around : ", str(round(os.path.getsize(save_path) / (1024 * 1024 * 1024), 2)), "G.")