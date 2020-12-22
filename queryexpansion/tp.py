# Temporal Proximity
import common
import time
import os
from itertools import combinations
from math_tool import sigmoid
from argparse import ArgumentParser
import json
from methods_dic import load_dic


def cal_time_diff_by_second(time1, time2):
    return abs(time1 - time2)


# load dic of latest modify time for all methods
def load_lmt_dic(proj_path, ss_dic):
    reversed_ss_dic = dict(zip(ss_dic.values(), ss_dic.keys()))
    id_method_dic, id_value_dic = ss_dic, dict()
    cache_dic = dict()
    not_in_list = []

    for root, dirs, files in os.walk(proj_path):
        for file in files:
            if not file.endswith(common.java_file_postfix):
                continue
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(common.afterPT_code_correspond_splitor)
                    method_signature, last_modify_time = parts[0], parts[-1]
                    if last_modify_time == 'null':
                        continue
                    # use relative path
                    relative_path = file_path.lstrip(proj_path)
                    key = '{}{}{}'.format(relative_path, common.path_sig_splitor, method_signature)
                    td = get_td(last_modify_time, cache_dic)

                    if key not in reversed_ss_dic:
                        if relative_path not in not_in_list:
                            not_in_list.append(relative_path)
                    else:
                        ssid = reversed_ss_dic[key]
                        id_method_dic[ssid] = key
                        id_value_dic[ssid] = td

    if not_in_list:
        print('calculate tp : ignore %d methods not in ss dic.' % len(not_in_list))
        print(not_in_list)
    return id_method_dic, id_value_dic


def get_td(last_modify_time, cache_dic):
    if last_modify_time in cache_dic:
        return cache_dic[last_modify_time]
    td = int(time.mktime(time.strptime(last_modify_time, common.time_format)))
    cache_dic[last_modify_time] = td
    return td


def cal_time_diff_for_dic(id_value_dic, save_path):
    keys = id_value_dic.keys()
    comb = combinations(keys, 2)
    print("Calculate methods of size : %d" % len(keys))

    time_sum, comb_length = 0, 0
    for ssid in comb:
        m1, m2 = ssid[0], ssid[1]
        time1, time2 = id_value_dic[m1], id_value_dic[m2]
        time_sum += abs(time1 - time2)
        comb_length += 1
    avg_td = float(time_sum / comb_length)

    cache_dic, tp_dic = dict(), dict()
    with open(save_path, 'w') as f:
        for ssid in comb:
            m1, m2 = ssid[0], ssid[1]
            time1, time2 = id_value_dic[m1], id_value_dic[m2]
            # if t1#t2 in result_dic, t2#t1 is in result_dic
            tp_cache_dic_key = '{}{}{}'.format(time1, common.tp_cache_dic_key_splitor, time2)
            if tp_cache_dic_key in cache_dic:
                tp_dic['{}{}{}'.format(m1, common.ss_key_splitor, m2)] = cache_dic[tp_cache_dic_key]
            else:
                diff = cal_time_diff_by_second(time1, time2)
                sig_time_diff = sigmoid(diff / avg_td)
                tp_cache_dic_key2 = '{}{}{}'.format(time2, common.tp_cache_dic_key_splitor, time1)
                cache_dic[tp_cache_dic_key] = sig_time_diff
                cache_dic[tp_cache_dic_key2] = sig_time_diff
                tp_dic['{}{}{}'.format(m1, common.ss_key_splitor, m2)] = sig_time_diff
        f.write(json.dumps(tp_dic))
    return


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-c", "--correspond_path", dest = "correspond_path", required = True)
    parser.add_argument("-s", "--save_path", dest = "save_path", required = True)
    parser.add_argument("-d", "--ss_dic_path", dest = "ss_dic_path", required = True)
    args = parser.parse_args()
    correspond_path = args.correspond_path
    save_path = args.save_path
    ss_dic_path = args.ss_dic_path

    start = time.process_time()
    print("Start Calculate Temporal Proximity...")

    ss_dic = load_dic(ss_dic_path)

    id_method_dic, id_value_dic = load_lmt_dic(correspond_path, ss_dic)
    cal_time_diff_for_dic(id_value_dic = id_value_dic, save_path = save_path)
    elapsed = round(time.process_time() - start, 2)
    print("Finished Calculate Temporal Proximity. Time used : %.2f seconds" % elapsed)
    print("Save to File : %s" % save_path)
    print("File size is around : %.2f MB." % round(os.path.getsize(save_path) / (1024 * 1024), 2))
