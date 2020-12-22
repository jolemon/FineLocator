# Semantic similarity
import numpy as np
import os
from argparse import ArgumentParser
from itertools import combinations
import time
from math_tool import cosine_similarity
import json
from methods_dic import update_methods_dic
import math
import re
import common


# delete blank space, "[[    " from head and "    ]]" from tail
def trim_vec_text(string):
    string = string.strip().lstrip("[[").rstrip("]]").strip()
    return re.sub(r',(\s*)', ',', string)


# read one line from br file and parse this line to a vector in shape of (1, dim)
def load_brv(file_path, dim):
    with open(file_path, 'r') as f:
        vec_text = f.readline()
        trim_vec = trim_vec_text(vec_text)
        arr = np.fromstring(string = trim_vec, sep = ',')
        vec = arr.reshape((-1, dim), order = 'C')
        return vec


def _load_cv_from_file(id_method_dic, id_value_dic, abs_file_path, dim, parent_dir):
    with open(abs_file_path, 'r') as f:
        lines = f.readlines()
        for k in range(0, len(lines)-1, 2):
            # k+1行: 函数签名
            signature = lines[k+1]
            signature = signature.strip().rstrip(common.code_tfidf_linesep)
            # remove parent_dir because the path is different with tp_dir and cd_dir.
            # There is already a "#" ahead of signature in code_tf-idf file, so don't need to append another "#"
            relative_path = abs_file_path.lstrip(parent_dir)
            signature = relative_path + signature

            # k行: code vector
            vec_text = lines[k]
            trim_vec = trim_vec_text(vec_text)
            arr = np.fromstring(string = trim_vec, sep = ',')
            vec = arr.reshape((-1, dim), order = 'C')
            update_methods_dic(signature, vec, id_method_dic, id_value_dic)
    return


def load_cv(dir_path, dim):
    id_method_dic, id_value_dic = dict(), dict()
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if not file.endswith(common.java_file_postfix):
                continue
            _load_cv_from_file(id_method_dic = id_method_dic, id_value_dic = id_value_dic,
                               abs_file_path = os.path.join(root, file), dim = dim, parent_dir = dir_path)
    return id_method_dic, id_value_dic


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-c", "--code_vector_dir", dest = "code_vector_dir", required = True)
    parser.add_argument("-d", "--dim", dest = "dim", required = True)
    parser.add_argument("-s", "--save_path", dest = "save_path", required = True)

    args = parser.parse_args()
    code_vector_dir = args.code_vector_dir
    dim = int(args.dim)
    save_path = args.save_path

    print("load code vector from directory: %s ..." % code_vector_dir)
    id_method_dic, id_value_dic = load_cv(dir_path = code_vector_dir, dim = dim)

    keys = id_method_dic.keys()
    print("Calculate methods of size : %d " % len(keys))
    comb_start_time = time.process_time()
    comb = combinations(keys, 2)
    comb_elapsed = round(time.process_time() - comb_start_time, 2)
    print("Combination time used : %.2f seconds" % comb_elapsed)

    print("Start Calculate Semantic Similarity...")
    cal_start_time = time.process_time()
    ss_dic = dict()
    for ss in comb:
        m1, m2 = ss[0], ss[1]
        vec1, vec2 = id_value_dic[m1], id_value_dic[m2]
        cs = cosine_similarity(vec1 = vec1, vec2 = vec2)
        if math.isnan(cs):
            cs = 0.0
        ss_dic['{}{}{}'.format(m1, common.ss_key_splitor, m2)] = cs
    cal_elapsed = round(time.process_time() - cal_start_time, 2)
    print("Finished calculate Semantic Similarity. Time used : %.2f seconds" % cal_elapsed)

    write_start_time = time.process_time()
    with open(save_path, 'w') as save_file:
        save_file.write(json.dumps(ss_dic))

    with open('{}.dic'.format(save_path), 'w') as dic_file:
        dic_file.write(json.dumps(id_method_dic))
    write_elapsed = round(time.process_time() - write_start_time, 2)
    print("Finished saving file. Time used : %.2f seconds" % write_elapsed)
    print("Save to file : %s" % save_path)
    print("File size is around : %.2f MB." % round(os.path.getsize(save_path) / (1024 * 1024), 2))
