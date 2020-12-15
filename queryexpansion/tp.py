# Temporal Proximity

import time
import os
from itertools import combinations
from math_tool import sigmoid
from argparse import ArgumentParser
import json

time_format = "%a %b %d %H:%M:%S %Z %Y"


def cal_time_diff_by_second(time1, time2):
    return abs(time1 - time2)


# load dic of last modify time for all methods
def load_dic_lmt(proj_path, ss_dic):
    # id_method_dic = dict()
    reversed_ss_dic = dict(zip(ss_dic.values(), ss_dic.keys()))
    id_method_dic = ss_dic
    id_value_dic = dict()

    cache_dic = dict()

    not_in_count = 0
    not_in_list = []

    for root, dirs, files in os.walk(proj_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                # print(file_path)
                f = open(file_path, 'r')
                lines = f.readlines()
                for line in lines:
                    if line is not None:
                        line = line.strip()
                        # parts = line.split(',')
                        parts = line.split('$')
                        method_signature = parts[0]
                        last_modify_time = parts[-1]
                        if last_modify_time == 'null':
                            continue
                        # use relative path
                        relative_path = file_path.replace(proj_path, "")
                        # key = relative_path + '#' + ','.join(method_signature)
                        key = relative_path + '#' + method_signature
                        td = get_td(last_modify_time, cache_dic)

                        if key in reversed_ss_dic:
                            ssid = reversed_ss_dic[key]
                            id_method_dic[ssid] = key
                            id_value_dic[ssid] = td
                        else:
                            file_name = key.split('#')[0]
                            if file_name not in not_in_list:
                                not_in_list.append(file_name)
                            not_in_count += 1
                            #print(key, 'not in ss dic')

                f.close()
    if not_in_count > 0 :
        print('calculate tp : ignore', not_in_count, 'methods not in ss dic.')
        print(not_in_list)
    return id_method_dic, id_value_dic


def get_td(last_modify_time, cache_dic):
    if last_modify_time in cache_dic:
        return cache_dic[last_modify_time]
    else:
        td = int(time.mktime(time.strptime(last_modify_time, time_format)))
        cache_dic[last_modify_time] = td
        return td


def cal_time_diff_for_dic(id_method_dic, id_value_dic, save_path):
    keys = id_value_dic.keys()
    comb_list = list(combinations(keys, 2))
    print("Calculate methods of size :", str(len(keys)))

    sum = 0
    for cb in comb_list:
        m1 = cb[0]
        m2 = cb[1]
        time1 = id_value_dic[m1]
        time2 = id_value_dic[m2]
        sum += abs(time1 - time2)
    avg_td = float( sum / len(comb_list) )

    cache_dic = dict()
    tp_dic = dict()
    with open(save_path, 'w') as f:
        for tp in comb_list:
            m1 = tp[0]
            m2 = tp[1]
            time1 = id_value_dic[m1]
            time2 = id_value_dic[m2]
            # if t1#t2 in result_dic, t2#t1 is in result_dic
            if (str(time1) + '#' + str(time2)) in cache_dic:
                tp_dic[str(m1) + "分" + str(m2)] = cache_dic[str(time1) + '#' + str(time2)]
                # f.write(m1 + "分"+ m2 + "分" + str(cache_dic[time_str1 + '#' + time_str2]) + "\n")
            else:
                diff = cal_time_diff_by_second(time1, time2)
                sig_time_diff = sigmoid(diff / avg_td)
                cache_dic[str(time1) + '#' + str(time2)] = sig_time_diff
                cache_dic[str(time2) + '#' + str(time1)] = sig_time_diff
                tp_dic[str(m1) + "分" + str(m2)] = sig_time_diff
                # f.write(m1 + "分"+ m2 + "分" + str(sig_time_diff) + "\n")
        f.write(json.dumps(tp_dic))
    # with open(save_path + ".dic", 'w') as dic_f:
    #     dic_f.write(json.dumps(id_method_dic))
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

    from methods_dic import load_dic
    # ss_dic
    ss_dic = load_dic(ss_dic_path)

    id_method_dic, id_value_dic = load_dic_lmt(correspond_path, ss_dic)
    cal_time_diff_for_dic(id_method_dic, id_value_dic, save_path = save_path)
    elapsed = round(time.process_time() - start, 2)
    print("Finished Calculate Temporal Proximity. Time used : ", elapsed, "s.")
    print("Save to File :", save_path)
    print("File size is around : ", str(round(os.path.getsize(save_path) / (1024 * 1024 ), 2)), "M.")