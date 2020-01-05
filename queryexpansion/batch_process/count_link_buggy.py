def load_linked_buggy_file(file, outer_splitor = '外', inner_splitor = '内', replace_splitor = '#'):
    import handle_cd_method
    dic = {}
    with open(file, 'r') as linked_buggy_file:
        for line in linked_buggy_file.readlines():
            line = line.strip()
            parts = line.split('\t')
            proj_id = parts[0]
            if proj_id not in dic:
                dic[proj_id] = []

            if outer_splitor not in parts[1]:
                method = parts[1].replace(inner_splitor, replace_splitor)
                method = handle_cd_method.trim_comma_in_paras(method)

                dic[proj_id].append(method)
            else:
                methods = parts[1].split(outer_splitor)
                for method in methods:
                    method = method.replace(inner_splitor, replace_splitor)
                    method = handle_cd_method.trim_comma_in_paras(method)
                    dic[proj_id].append(method)

    return dic


def load_prediction_file(proj, dir, find_tag = '$1$', splitor = '$'):
    import os
    dic = {}
    for file in os.listdir(dir):
        if file == '.DS_Store':
            continue
        with open(os.path.join(dir,file), 'r') as prediction_file:
            for line in prediction_file.readlines():
                line = line.strip()
                if find_tag not in line:
                    continue
                else:
                    parts = line.split(splitor)
                    proj_id = parts[0]
                    # predict_res = parts[1]
                    sig = parts[3]
                    if proj_id not in dic:
                        dic[proj_id] = []
                    dic[proj_id].append(proj + '/' + proj_id + sig)
    return dic


def batch_run():
    projs = ['Math'] #'Time', 'Mockito', 'Lang', 'Math', 'Closure'
    abr = '1000'

    from handle_cd_method import trim_method
    for proj in projs:
        linked_buggy_file = linked_buggy_dir + proj + linked_buggy_postfix
        predict_result_file = predict_result_dir + proj + '/' + proj + abr

        dic = load_linked_buggy_file(linked_buggy_file)
        res_dic = load_prediction_file(proj, predict_result_file)
        for item in dic:
            if item not in res_dic:
                print(item, 'not found in result')
                print(sorted(dic[item]))
                continue

            ori_len = len(dic[item])
            res_len = len(res_dic[item])
            if ori_len != res_len:
                print(item, 'ori_num:', ori_len, 'res_num:', res_len)

                print('ori', sorted(dic[item]))
                print('res', sorted(res_dic[item]))
                print('lack:')
                for method in dic[item]:
                    if method not in res_dic[item]:
                        print(method)

linked_buggy_dir = '/Users/lienming/Downloads/final_defects4j/linked-bugMethods/'
linked_buggy_postfix = '_bugId_buggyMethodsName'
predict_result_dir = '/Users/lienming/abr/' #Downloads/expres/all/
batch_run()