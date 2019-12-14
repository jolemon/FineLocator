import json

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


def update_id_method_dic(id_method_dic, method_id_dic, method):
    if method not in method_id_dic:
        new_id = len(id_method_dic) + 1
        id_method_dic[new_id] = method
        method_id_dic[method] = new_id
        return new_id
    # if method not in id_method_dic.values():
    #     new_id = len(id_method_dic)+1
    #     id_method_dic[new_id] = method
    #     return new_id
    else:
        return method_id_dic[method]
        # return find_k_by_v(id_method_dic, method)


def load_dic(path):
    with open(path, 'r') as f:
        dic = json.loads(f.read())
    return dic


def write_dic(path, dic):
    with open(path, 'w') as f:
        f.write(json.dumps(dic))
    return


def find_k_by_v(dic, value):
    k_list = [k for k, v in dic.items() if v == value]
    if len(k_list) > 0:
        return k_list[0]
    else:
        return None


def compare_dic(dic1, dic2):
    len1 = len(dic1)
    len2 = len(dic2)
    if len1 != len2:
        print('length:', len1, len2)
        return False
    else:
        for key in dic1:
            if key not in dic2:
                print('key:', key, 'not exists')
                return False
            else:
                v1 = dic1[key]
                v2 = dic2[key]
                if  v1 != v2:
                    print('key =', key, 'v1 =', v1, 'v2 =', v2)
                    return False
                continue
        return True

# dic1 = {1:'aaa', 2:'bbb', 3:'ccc'}
# dic2 = {1:'aaa', 2:'bbb', 3:'ccc'}
# dic3 = {1:'aaa', 2:'bb', 3:'ccc'}
# print(compare_dic(dic1, dic3))

# dic = {1:0.1, 2:0.2}
# import json
# with open('test.dic', 'w') as f:
#     f.write(json.dumps(dic))
#
# with open('test.dic', 'r') as ff :
#     ss_dic = json.loads(ff.read())
#
# print(ss_dic["1"])




