# Semantic similarity
import numpy as np
import os
from argparse import ArgumentParser
from itertools import combinations
import time
from math_tool import cosine_similarity
from methods_dic import update_methods_dic
import math
import common
from tp import get_td, cal_time_diff_by_second, sigmoid
from ss import trim_vec_text


def load_cv_tp(code_vec_dir, correspond_dir, dim):
    id2sig_dic, id2sstp_dic = dict(), dict()
    tp_cache_dic = dict()
    tp_not_in_ss_list = []
    for root, dirs, files in os.walk(code_vec_dir):
        for file in files:
            code_vec_path = os.path.join(root, file)
            correspond_path = code_vec_path.replace(code_vec_dir, correspond_dir)
            if not file.endswith(common.java_file_postfix) or not os.path.exists(correspond_path):
                continue
            tmp_ss_dic = dict()
            with open(code_vec_path, 'r') as cv_file, open(correspond_path, 'r') as tp_file:
                # 读该文件下code vector并缓存到tmp_ss_dic
                cv_lines = cv_file.readlines()
                for k in range(0, len(cv_lines) - 1, 2):
                    # k+1行: 函数签名
                    signature = cv_lines[k + 1]
                    signature = signature.strip().rstrip(common.code_tfidf_linesep)
                    # remove parent_dir because the path is different with tp_dir and cd_dir.
                    # There is already a "#" ahead of signature in code_tf-idf file, so don't need to append another "#"
                    relative_path = code_vec_path.lstrip(code_vec_dir)
                    signature = relative_path + signature

                    # k行: code vector
                    vec_text = cv_lines[k]
                    trim_vec = trim_vec_text(vec_text)
                    arr = np.fromstring(string = trim_vec, sep = ',')
                    vec = arr.reshape((-1, dim), order = 'C')
                    tmp_ss_dic[signature] = vec

                # 读对应correspond文件, 并筛选出存在于tmp_ss_dic中的tp
                tp_lines = tp_file.readlines()
                for tp_line in tp_lines:
                    tp_line = tp_line.strip()
                    if not tp_line:
                        continue
                    parts = tp_line.split(common.afterPT_code_correspond_splitor)
                    signature, last_modify_time = parts[0], parts[-1]
                    if last_modify_time == 'null':
                        continue
                    # use relative path
                    relative_path = correspond_path.lstrip(correspond_dir)
                    key = '{}{}{}'.format(relative_path, common.path_sig_splitor, signature)
                    if key not in tmp_ss_dic:
                        if relative_path not in tp_not_in_ss_list:
                            tp_not_in_ss_list.append(relative_path)
                        continue
                    td = get_td(last_modify_time, tp_cache_dic)
                    update_methods_dic(key, (vec, td), id2sig_dic, id2sstp_dic)

    if tp_not_in_ss_list:
        print('calculate tp : ignore %d methods not in ss dic.' % len(tp_not_in_ss_list))
        print(tp_not_in_ss_list)
    return id2sig_dic, id2sstp_dic


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-c", "--code_vector_dir", dest = "code_vector_dir", required = True)
    parser.add_argument("-cr", "--correspond_dir", dest = "correspond_dir", required = True)
    parser.add_argument("-d", "--dim", dest = "dim", required = True)
    parser.add_argument("-s", "--save_path", dest = "save_path", required = True)

    args = parser.parse_args()
    code_vec_dir = args.code_vector_dir
    correspond_dir = args.correspond_dir
    dim = int(args.dim)
    save_path = args.save_path

    id2sig_dic, id2sstp_dic = load_cv_tp(code_vec_dir = code_vec_dir, correspond_dir = correspond_dir, dim = dim)
    keys = id2sig_dic.keys()
    print("Calculate methods of size : %d " % len(keys))
    if len(keys) == 0:
        exit(1)
    comb = combinations(keys, 2)

    print("Start Calculate Semantic Similarity & Temporal Proximity")
    cal_start_time = time.process_time()

    # 计算Temporal Proximity平均值
    time_sum, comb_length = 0, 0
    for id1, id2 in comb:
        (vec1, time1), (vec2, time2) = id2sstp_dic[id1], id2sstp_dic[id2]
        time_sum += abs(time1 - time2)
        comb_length += 1
    avg_td = float(time_sum / comb_length)
    print("Temporal Proximity平均值: ", avg_td)

    tp_cache_dic, ss_dic, tp_dic = dict(), dict(), dict()
    save_file = open(save_path, 'w')
    comb = combinations(keys, 2)
    write_line_count = 0
    for id1, id2 in comb:
        (vec1, time1), (vec2, time2) = id2sstp_dic[id1], id2sstp_dic[id2]
        # 计算ss
        cs = cosine_similarity(vec1 = vec1, vec2 = vec2)
        if math.isnan(cs):
            cs = 0.0

        # 计算tp
        tp_cache_dic_key = '{}{}{}'.format(time1, common.tp_cache_dic_key_splitor, time2)
        if tp_cache_dic_key not in tp_cache_dic:
            diff = cal_time_diff_by_second(time1, time2)
            sig_time_diff = sigmoid(diff / avg_td)
            tp_cache_dic_key2 = '{}{}{}'.format(time2, common.tp_cache_dic_key_splitor, time1)
            tp_cache_dic[tp_cache_dic_key] = sig_time_diff
            tp_cache_dic[tp_cache_dic_key2] = sig_time_diff
        tp = tp_cache_dic[tp_cache_dic_key]

        sstp_key = '{}{}{}'.format(id1, common.ss_key_splitor, id2)
        save_file.write('{}{}{}{}{}{}'.format(sstp_key, common.sstp_external_splitor,
                                              cs, common.sstp_internal_splitor, tp, common.linesep))
        write_line_count += 1
        if write_line_count >= common.flush_size:
            save_file.flush()
            write_line_count = 0
    save_file.flush()
    save_file.close()
    cal_elapsed = round(time.process_time() - cal_start_time, 2)
    print("Finished calculate Semantic Similarity & Temporal Proximity. Time used : %.2f seconds" % cal_elapsed)

    with open('{}.dic'.format(save_path), 'w') as dic_file:
        for sid, sig in id2sig_dic.items():
            dic_file.write('{}{}{}{}'.format(sid, common.id2sig_splitor, sig, common.linesep))

    print("Save to file : %s" % save_path)
    print("File size is around : %.2f MB." % round(os.path.getsize(save_path) / (1024 * 1024), 2))
