from argparse import ArgumentParser
import json
import time
from handle_cd_method import trim_template_T, trim_method, trim_ss_signature
from ss import load_cv, load_brv
import rank
from methods_dic import load_dic
import common


def find_v_by_sharp_k(sharp_key_pair, key_id_dic, cd_dic, cd_sig2id_dic, used_cd_dic):
    parts = sharp_key_pair.split(common.ss_key_splitor)
    m0, m1 = parts[0], parts[1]
    m0_sig, m1_sig = trim_ss_signature(key_id_dic[m0]), trim_ss_signature(key_id_dic[m1])

    # step 1 : remove "@* " and function modifier and "throws *"
    # trim_m0, trim_m1 = trim_method(m0_sig), trim_method(m1_sig)

    # step 2 : try to find new key in dic again
    if m0_sig in cd_sig2id_dic and m1_sig in cd_sig2id_dic:
        m0_id, m1_id = cd_sig2id_dic[m0_sig], cd_sig2id_dic[m1_sig]
        key = '{}{}{}'.format(m0_id, common.ss_key_splitor, m1_id)
        if key in cd_dic:
            used_cd_dic[key] = '{}{}{}'.format(m0_sig, common.ss_key_splitor, m1_sig)
            return cd_dic[key]
        else:
            reversed_key = '{}{}{}'.format(m1_id, common.ss_key_splitor, m0_id)
            if reversed_key not in cd_dic:
                return 0
            used_cd_dic[reversed_key] = '{}{}{}'.format(m0_sig, common.ss_key_splitor, m1_sig)
            return cd_dic[reversed_key]
    else:
        return 0


def calculate_ac(ss_path, tp_path, cd_path, save_path):
    ac_dic = dict()
    ss_dic, tp_dic, cd_dic = load_dic(ss_path), load_dic(tp_path), load_dic(cd_path)
    ss_id_dic, cd_id2sig_dic = load_dic('{}.dic'.format(ss_path)), load_dic('{}.dic'.format(cd_path))
    tp_id_dic = ss_id_dic
    # convert dict
    cd_sig2id_dic = dict(zip(cd_id2sig_dic.values(), cd_id2sig_dic.keys()))

    used_cd_dic = {}
    for tp_key, tp_value in tp_dic.items():
        if tp_key not in ss_dic:
            # '1#2' in, but '2#1' not in?
            # print(tp_key, 'not in ss_dic')
            continue
        ss_value = ss_dic[tp_key]
        ac_value = alpha * ss_value
        ac_value += beta * tp_value if beta > 0 else 0
        if gamma > 0:
            cd_value = find_v_by_sharp_k(sharp_key_pair = tp_key, key_id_dic = tp_id_dic, cd_dic = cd_dic,
                                         cd_sig2id_dic = cd_sig2id_dic, used_cd_dic = used_cd_dic)
            ac_value += gamma * cd_value
        ac_dic[tp_key] = ac_value

    cd_dic_not_used_num = len(cd_dic) - len(used_cd_dic)
    if cd_dic_not_used_num > 0 and gamma > 0:
        print('total cd_dic num: %d ; cd_dic not used num: %d ' % (len(cd_dic), cd_dic_not_used_num))
    print("ac size: %d" % len(ac_dic))
    avg_ac = float(sum(ac_dic.values()) / len(ac_dic))
    print("average augmentation coefficient is %f" % avg_ac)

    # before method augmentation, filter ac that is lower than avg_ac.
    # list(ac_dic.keys()) 另存一个变量，重新申请内存空间
    for ac_key in list(ac_dic.keys()):
        if ac_dic[ac_key] < avg_ac:
            del ac_dic[ac_key]
    return ac_dic


def method_augmentation(cv_path, ac_dic):
    id_method_dic, id_value_dic = load_cv(cv_path, dim)

    result_dic = dict()
    for ac_key, ac_value in ac_dic.items():
        ids = ac_key.split(common.ss_key_splitor)
        id1, id2 = int(ids[0]), int(ids[1])
        doc_vector1, doc_vector2 = id_value_dic[id1], id_value_dic[id2]

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


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-ss", "--ss_path", dest = "ss_path", required = True)
    parser.add_argument("-tp", "--tp_path", dest = "tp_path", required = True)
    parser.add_argument("-cd", "--cd_path", dest = "cd_path", required = True)
    parser.add_argument("-c",  "--code_vector_dir", dest = "code_vector_dir", required = True)
    parser.add_argument("-s",  "--save_path", dest = "save_path", required = True)
    parser.add_argument("-b",  "--br_path", dest = "br_path", required = True)
    parser.add_argument("-i",  "--br_id", dest = "br_id",   required = True)
    parser.add_argument("-l",  "--link_buggy_path", dest = "link_buggy_path", required = True)
    parser.add_argument("-d",  "--dim", dest = "dim",     required = True)
    parser.add_argument("-e",  "--epochs",  dest = "epochs",  required = True)
    parser.add_argument("-alpha", "--alpha", dest = "alpha", required = True)
    parser.add_argument("-beta", "--beta", dest = "beta", required = True)
    parser.add_argument("-gamma", "--gamma", dest = "gamma", required = True)
    args = parser.parse_args()
    ss_path, tp_path, cd_path = args.ss_path, args.tp_path, args.cd_path
    code_vector_dir = args.code_vector_dir
    br_path = args.br_path
    br_id = args.br_id
    link_buggy_path = args.link_buggy_path
    save_path = args.save_path
    dim = int(args.dim)
    epochs = int(args.epochs)
    alpha, beta, gamma = float(args.alpha), float(args.beta), float(args.gamma)

    start = time.process_time()
    print("Start to Calculate Query Expansion...")
    ac_dic = calculate_ac(ss_path = ss_path, tp_path = tp_path, cd_path = cd_path, save_path = save_path)
    if not ac_dic:
        exit(1)

    id_dic, id_value_dic = method_augmentation(cv_path = code_vector_dir, ac_dic = ac_dic)

    # Rank
    br_vector = load_brv(file_path = br_path, dim = dim)
    rel_list = rank.cal_rel(br_vector, id_value_dic)
    link_dic = rank.load_link_dic(link_buggy_path)
    buggy_method_list = link_dic[br_id]
    # 输出格式与iBug项目一致，则可以复用iBug计算TopK、MAP、MRR的代码
    # 输出格式： bug报告ID$真实标签$计算相关度$路径方法名
    result_list = ['{}${}${}${}'.format(br_id, x[1],
                                        (0, 1)[trim_method(trim_template_T(id_dic[x[0]])) in buggy_method_list],
                                        trim_template_T(id_dic[x[0]])) for x in rel_list]

    proj_id = br_id
    abrstr = '{}{}{}'.format(int(10 * alpha), int(10 * beta), int(10 * gamma))
    save_path = '{}/{}_{}_{}_{}'.format(save_path, proj_id, dim, epochs, abrstr)
    with open(save_path, 'w') as f:
        f.write(common.linesep.join(result_list))

    elapsed = round(time.process_time() - start, 2)
    print("Finished Calculate Semantic Similarity. Time used : %.2f seconds" % elapsed)

    # import subprocess
    # subprocess.call(['./zou_cal_HitK-MAP-MRR.sh', save_path])
