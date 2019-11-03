# use :
#      id_methods_dic = {id : method}
#             vec_dic = {id : vec}
# to record methods,
# so that reduce the cost of disk storage and memory use.
def build_methods_dic(method, value, id_method_dic, id_value_dic):
    if method not in id_method_dic.values():
        new_id = len(id_method_dic)+1
        id_method_dic[new_id] = method
        id_value_dic[new_id] = value
    else:
        print(method, 'already in id_method_dic.')
    return


def update_id_method_dic(id_method_dic, method):
    if method not in id_method_dic.values():
        new_id = len(id_method_dic)+1
        id_method_dic[new_id] = method
        return new_id
    else:
        return find_k_by_v(id_method_dic, method)


def find_k_by_v(dic, value):
    k_list = [k for k, v in dic.items() if v == value]
    if len(k_list) > 0:
        return k_list[0]
    else:
        return None


# dic = {1:0.1, 2:0.2}
# import json
# with open('test.dic', 'w') as f:
#     f.write(json.dumps(dic))
#
# with open('test.dic', 'r') as ff :
#     ss_dic = json.loads(ff.read())
#
# print(ss_dic["1"])




