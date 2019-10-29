from argparse import ArgumentParser
import json
import time
from handle_cd_method import trim_method


alpha = 0.8
beta = 0.1
gamma = 0.1

function_modifier_list = ['public', 'private', 'final', 'static', 'abstract',
                          'protected', 'synchronized', 'native', 'transient', 'volatie']

# TODO 计算平均值
def cal_average_augmentation_coefficient():
    return 0


# ss, tp key = ${method1}"#"${method2}, cd key = turple(method1, method2)
def method_augmentation(ss_path, tp_path, cd_path, save_path):
    ac_dic = dict()
    with open(ss_path, 'r') as ss_file, open(tp_path, 'r') as tp_file, open(cd_path, 'r') as cd_file, \
         open('cd_error.log', 'w') as cd_error_file, open(save_path, 'w') as succ_file:
        ss_dic = json.loads(ss_file.read())
        tp_dic = json.loads(tp_file.read())
        cd_dic = json.loads(cd_file.read())
        print("load ss, tp, cd dictionary ready.")
        for tp_key in tp_dic:
            tp_value = tp_dic[tp_key]
            ss_value = find_v_by_sharp_k(tp_key, ss_dic)
            if ss_value is None:
                # print("failed to find semantic similarity for", tp_key)
                # ss_error_file.write(tp_key + "\n")
                continue
            cd_value = find_v_by_sharp_k(tp_key, cd_dic)
            if cd_value is None:
                # print("failed to find call dependency for", tp_key)
                cd_error_file.write(tp_key + "\n")
                continue
            ac_value = alpha * ss_value + beta * tp_value + gamma * cd_value
            ac_dic[tp_key] = ac_value
            succ_file.write(tp_key + "  " + str(ac_value) + "\n")
            # print(tp_key, ac_value)
    return


# key = m1#m2
def find_v_by_sharp_k(key, dic, flag = True):
    if key in dic:
        return dic[key]
    else:
        parts = key.split('分')
        m0 = parts[0]
        m1 = parts[1]
        switch_key = m1 + '分' + m0
        if switch_key in dic:
            return dic[switch_key]
        else:
            if flag is True:
                # step 1 : remove "@* " and function modifier
                trim_m0 = trim_method(m0)
                trim_m1 = trim_method(m1)
                # step 2 : try to find new key in dic again
                new_key = trim_m0 + '分' + trim_m1
                return find_v_by_sharp_k(new_key, dic, flag = False)
            else:
                return None



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