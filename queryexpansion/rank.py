import math_tool
import json
from handle_cd_method import trim_comma_in_paras, trim_method


def cal_single_rel(bug_report_vector, augmented_method_vector):
    return math_tool.cosine_similarity(bug_report_vector, augmented_method_vector)


def load_augmentation_methods(path):
    with open(path, 'r') as f:
        dic = json.loads(f.read())
    return dic


def cal_rel(brv, dic):
    result_dic = dict()
    for key in dic:
        rel_value = cal_single_rel(brv, dic[key])
        result_dic[key] = rel_value

    ranked_dic = _rank_dic(result_dic)
    return ranked_dic


def _rank_dic(dic):
    sorted_dic = sorted(dic.items(), key = lambda x : x[1], reverse = True)
    return sorted_dic


# read "link_buggyMethods/xxx" file and return a dictionary
def load_link_dic(path):
    dic = {}
    f = open(path, 'r')
    lines = f.readlines()
    for line in lines:
        line = line.strip()
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
                path =  '/'+'/'.join((pm_parts[0].split('/'))[2:])
                method = pm_parts[1]

                path_method = path + '#' + trim_method(trim_comma_in_paras(method))

                if br_id not in dic:
                    dic.setdefault(br_id, []).append(path_method)
                else:
                    dic[br_id].append(path_method)
    return dic

# for item in ['Closure']: #'Time', 'Mockito', 'Lang', 'Math'
#     dic = load_link_dic("/Users/lienming/Downloads/final_defects4j/linked-bugMethods/" + item + "_bugId_buggyMethodsName")
# for ms in dic['Time_3']:
#     print(ms)



