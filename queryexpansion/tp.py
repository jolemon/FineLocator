import time
import os
from itertools import combinations

time_format = "%a %b %d %H:%M:%S %Z %Y"


def cal_time_diff_by_second(time_str1, time_str2):
    seconds1 = time.mktime(time.strptime(time_str1, time_format))
    seconds2 = time.mktime(time.strptime(time_str2, time_format))
    return abs(seconds1-seconds2)


# load dic of last modify time for all methods
def load_dic_lmt(proj_path):
    dic = {}
    for root, dirs, files in os.walk(proj_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                print(file_path)
                f = open(file_path, 'r')
                lines = f.readlines()
                for line in lines:
                    if line is not None:
                        line = line.strip()
                        parts = line.split(',')
                        method_signature = parts[0]
                        last_modify_time = parts[-1]
                        key = file_path + '#' + method_signature
                        dic[key] = last_modify_time
    return dic


def cal_time_diff_for_dic(dic):
    comb_list = list(combinations(dic.keys(), 2))
    print(len(comb_list))
    # for tp in comb_list:
    #     m1 = tp[0]
    #     m2 = tp[1]
    #     time_str1 = dic[m1]
    #     time_str2 = dic[m2]
    #     diff = cal_time_diff_by_second(time_str1, time_str2)
    #     print(diff)
    return


time_dic = load_dic_lmt("/Users/lienming/FineLocator/expRes/afterPT/correspond/Time/Time_4")
cal_time_diff_for_dic(time_dic)

