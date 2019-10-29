from argparse import ArgumentParser
import json
import time

alpha = 0.8
beta = 0.1
gamma = 0.1

# TODO 计算平均值
def cal_average_augmentation_coefficient():
    return 0


# ss, tp key = ${method1}"#"${method2}, cd key = turple(method1, method2)
def method_augmentation(ss_path, tp_path, cd_path, save_path):
    ac_dic = dict()
    with open(ss_path, 'r') as ss_file, open(tp_path, 'r') as tp_file, open(cd_path, 'r') as cd_file:
        ss_dic = json.loads(ss_file.read())
        tp_dic = json.loads(tp_file.read())
        cd_dic = json.loads(cd_file.read())
        print("load ss, tp, cd dictionary ready.")
        for tp_key in tp_dic:
            tp_value = tp_dic[tp_key]
            ss_value = find_v_by_sharp_k(tp_key, ss_dic)
            if ss_value is None:
                print("failed to find semantic similarity for", tp_key)
                continue
            cd_value = find_v_by_sharp_k(tp_key, cd_dic)
            if cd_value is None:
                print("failed to find call dependency for", tp_key)
                continue
            ac_value = alpha * ss_value + beta * tp_value + gamma * cd_value
            ac_dic[tp_key] = ac_value
            print(tp_key, ac_value)
    print(len(ac_dic))
    return


# key = m1#m2
def find_v_by_sharp_k(key, dic):
    if key in dic:
        return dic[key]
    else:
        parts = key.split('分')
        switch_key = parts[1] + '分' + parts[0]
        if switch_key not in dic:
            return
        else:
            return dic[switch_key]



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-ss", "--ss_path", dest = "ss_path", required = True)
    parser.add_argument("-tp", "--tp_path", dest = "tp_path", required = True)
    parser.add_argument("-cd", "--cd_path", dest = "cd_path", required = True)
    parser.add_argument("-s", "--save_path", dest = "save_path", required = True)

    args = parser.parse_args()
    ss_path = args.ss_path
    tp_path = args.tp_path
    cd_path = args.cd_path
    save_path = args.save_path

    start = time.process_time()
    print("Finally, Start to Calculate Query Expansion...")
    method_augmentation(ss_path = ss_path, tp_path = tp_path, cd_path = cd_path, save_path = save_path)
    elapsed = round(time.process_time() - start, 2)
    print("Finished Calculate Query Expansion. Time used : ", elapsed, "s.")