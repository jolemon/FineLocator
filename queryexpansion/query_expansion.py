from argparse import ArgumentParser
import json
import time
from handle_cd_method import trim_template_T, trim_method, trim_ss_signature
from ss import load_cv, load_brv
import rank
from methods_dic import load_dic, compare_dic


def find_v_by_sharp_k(sharp_key_pair, key_id_dic, cd_dic, cd_sig2id_dic, used_cd_dic):
    parts = sharp_key_pair.split('分')
    m0 = parts[0]
    m1 = parts[1]
    m0_sig = trim_ss_signature(key_id_dic[m0])
    m1_sig = trim_ss_signature(key_id_dic[m1])

    # step 1 : remove "@* " and function modifier and "throws *"
    # trim_m0 = trim_method(m0_sig)
    # trim_m1 = trim_method(m1_sig)

    # step 2 : try to find new key in dic again

    if m0_sig in cd_sig2id_dic and m1_sig in cd_sig2id_dic:
        m0_id = cd_sig2id_dic[m0_sig]
        m1_id = cd_sig2id_dic[m1_sig]

        key = m0_id + '分' + m1_id
        if key in cd_dic:
            used_cd_dic[key] = m0_sig + '分' + m1_sig
            return cd_dic[key]
        else:
            reversed_key = m1_id + '分' + m0_id
            if reversed_key in cd_dic:
                used_cd_dic[reversed_key] = m0_sig + '分' + m1_sig
                return cd_dic[reversed_key]
            else:
                return 0
    else:
        return 0


def calculate_ac(ss_path, tp_path, cd_path, save_path):
    ac_dic = dict()
    ss_dic = load_dic(ss_path)
    ss_id_dic = load_dic(ss_path + '.dic')
    tp_dic = load_dic(tp_path)
    # tp_id_dic = load_dic(tp_path + '.dic')
    tp_id_dic = ss_id_dic
    cd_dic = load_dic(cd_path)
    cd_id2sig_dic = load_dic(cd_path + '.dic')

    # convert dict
    cd_sig2id_dic = dict(zip(cd_id2sig_dic.values(), cd_id2sig_dic.keys()))

    print("load ss, tp, cd dictionary ready.")
    #check tp/ss dic
    # if not compare_dic(tp_id_dic, ss_id_dic):
    #     print("check tp/ss_dic exception!")
    #     return
    # else:
    #     print("check tp/ss_dic is same.")

    used_cd_dic = {}

    for tp_key in tp_dic:
        tp_value = tp_dic[tp_key]
        if tp_key in ss_dic:
            ss_value = ss_dic[tp_key]
        else:
            print(tp_key, 'not in ss_dic')
            continue
        cd_value = find_v_by_sharp_k(tp_key, tp_id_dic, cd_dic,
                                     cd_sig2id_dic = cd_sig2id_dic, used_cd_dic = used_cd_dic )

        ac_value = alpha * ss_value + beta * tp_value + gamma * cd_value
        ac_dic[tp_key] = ac_value

    for item in cd_dic:
        if item not in used_cd_dic:
            # print(item)
            parts = item.split('分')
            print(cd_id2sig_dic[parts[0]])
            print(cd_id2sig_dic[parts[1]])
            print()

    print('no used num:' , len(cd_dic)-len(used_cd_dic))
    print("ac size:", len(ac_dic))

    avg_ac = float(sum(ac_dic.values()) / len(ac_dic))

    print("average augmentation coefficient is", avg_ac)

    # before method augmentation, filter ac that is lower than avg_ac.
    # list(ac_dic.keys()) 另存一个变量，重新申请内存空间
    for ac_key in list(ac_dic.keys()):
        if ac_dic[ac_key] < avg_ac:
            del ac_dic[ac_key]

    return ac_dic


def method_augmentation(cv_path, ac_dic):
    id_method_dic, id_value_dic = load_cv(cv_path)

    result_dic = dict()
    for ac_key in ac_dic:
        ids = ac_key.split("分")
        ac_value = ac_dic[ac_key]
        id1 = int(ids[0])
        id2 = int(ids[1])

        doc_vector1 = id_value_dic[id1]
        doc_vector2 = id_value_dic[id2]

        if id1 not in result_dic:
            result_dic[id1] = doc_vector1 + doc_vector2 * ac_value
        else:
            result_dic[id1] += doc_vector2 * ac_value

        if id2 not in result_dic:
            result_dic[id2] = doc_vector2 + doc_vector1 * ac_value
        else:
            result_dic[id2] += doc_vector1 * ac_value
    id_value_dic.update(result_dic)

    return id_method_dic, id_value_dic


def load_ac_dic(path):
    with open(path + ".acdic", 'r') as f:
        dic = json.loads(f.read())
    return dic


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-ss", "--ss_path", dest = "ss_path", required = True)
    parser.add_argument("-tp", "--tp_path", dest = "tp_path", required = True)
    parser.add_argument("-cd", "--cd_path", dest = "cd_path", required = True)
    parser.add_argument("-c",  "--code_vector_dir", dest = "code_vector_dir", required = True)
    parser.add_argument("-s",  "--save_path", dest = "save_path", required = True)
    parser.add_argument("-b",  "--br_path", dest = "br_path", required = True)
    parser.add_argument("-i",  "--br_id"  , dest = "br_id",   required = True)
    parser.add_argument("-l",  "--link_buggy_path", dest = "link_buggy_path", required = True)
    parser.add_argument("-d",  "--dim"    , dest = "dim",     required = True)
    parser.add_argument("-e",  "--epochs",  dest = "epochs",  required = True)
    parser.add_argument("-alpha", "--alpha", dest = "alpha", required = True)
    parser.add_argument("-beta", "--beta", dest = "beta", required = True)
    parser.add_argument("-gamma", "--gamma", dest = "gamma", required = True)
    args = parser.parse_args()
    ss_path = args.ss_path
    tp_path = args.tp_path
    cd_path = args.cd_path
    code_vector_dir = args.code_vector_dir
    br_path = args.br_path
    br_id = args.br_id
    link_buggy_path = args.link_buggy_path
    save_path = args.save_path
    dim = int(args.dim)
    epochs = int(args.epochs)
    alpha = float(args.alpha)
    beta  = float(args.beta)
    gamma = float(args.gamma)

    start = time.process_time()
    print("Start to Calculate Query Expansion...")
    ac_dic = calculate_ac(ss_path = ss_path, tp_path = tp_path, cd_path = cd_path, save_path = save_path)
    if ac_dic is None:
        exit(1)

    id_dic, id_value_dic = method_augmentation(cv_path = code_vector_dir, ac_dic = ac_dic)

    # Rank
    br_vector = load_brv(br_path, dim = dim)
    rel_list = rank.cal_rel(br_vector, id_value_dic)
    link_dic = rank.load_link_dic(link_buggy_path)
    buggy_method_list = link_dic[br_id]
    # 输出格式与iBug项目一致，则可以复用iBug计算TopK、MAP、MRR的代码
    # 输出格式： bug报告ID$真实标签$计算相关度$路径方法名
    result_list = [ br_id + '$' +
                    str(x[1]) + '$' +
                    str((0, 1)[trim_method(trim_template_T(id_dic[x[0]])) in buggy_method_list]) + '$' +
                    trim_template_T(id_dic[x[0]])
                    for x in rel_list ]

    proj_id = br_id
    abrstr = str(int(10 * alpha)) + str(int(10 * beta)) + str(int(10 * gamma))
    save_path = save_path + '/' + proj_id + '_' + str(dim) + '_' + str(epochs) + '_' + abrstr
    with open(save_path, 'w') as f:
        f.write('\n'.join(result_list))


    elapsed = round(time.process_time() - start, 2)
    print("Finished Calculate Query Expansion. Time used : ", elapsed, "s.")

    
    # import subprocess
    # subprocess.call(['./zou_cal_HitK-MAP-MRR.sh', save_path])
