import math_tool
from ss import load_brv
import json


def cal_single_rel(bug_report_vector, augmented_method_vector):
    return math_tool.cosine_similarity(bug_report_vector, augmented_method_vector)


def load_augmentation_methods(path):
    with open(path, 'r') as f:
        dic = json.loads(f.read())
    return dic


def load_br_vector(path, dim):
    return load_brv(path, dim = dim)


def cal_rel(brv, dic):
    result_dic = dict()
    for key in dic:
        rel_value = cal_single_rel(brv, dic[key])
        result_dic[key] = rel_value
    return result_dic


# read "link_buggyMethods/xxx" file and return a dictionary
def load_link_dic(path, parent_name_for_path):
    dic = {}
    f = open(path, 'r')
    while True:
        line = f.readline()
        if not line:
            break
        if len(line) > 0:
            parts = line.split('\t')
            br_id = parts[0]
            pm_lists_str = parts[1].rstrip('\n')
            pm_lists = pm_lists_str.split('外')
            for pm_list in pm_lists:
                pm_parts = pm_list.split('内')
                if len(pm_parts) < 2:
                    print(pm_parts, "in this sentence can not find PATH / METHOD_NAME !")
                    continue
                path = parent_name_for_path + '/' + str(pm_parts[0])
                method = pm_parts[1]

                method_parts = method.split(' ')
                ret_type = method_parts[0]
                if ret_type.endswith('[]'):
                    new_method = ret_type[:-2] + ' '
                    for i in range(1, len(method_parts)):
                        new_method += method_parts[i] + ' '
                    new_method = new_method.strip()
                    path_method = path + '#' + new_method
                else:
                    path_method = path + '#' + method

                if br_id not in dic:
                    dic.setdefault(br_id, []).append(path_method)
                else:
                    dic[br_id].append(path_method)
    return dic


# 输出格式与iBug项目一致，则可以复用iBug计算TopK、MAP、MRR的代码
# 输出格式： bug报告ID$真实标签$计算相关度$路径方法名
