from argparse import ArgumentParser
import time
from handle_cd_method import trim_template_T, trim_method, trim_ss_signature
from ss import load_brv
import rank
from methods_dic import load_dic, file_iterator, load_csv_as_dic
import common
from query_expansion import find_v_by_sharp_k
import numpy as np


def calculate_ac(sstp_path, cd_path, ac_save_path):
    """
    读sstp计算ac并保存所有ac到文件
    :param sstp_path:
    :param cd_path:
    :param ac_save_path:
    :return:
    """
    sstp_id_dic = load_dic('{}.dic'.format(sstp_path))
    sstp_itr = file_iterator(sstp_path)
    cd_id2sig_dic, cd_dic = load_dic('{}.dic'.format(cd_path)), load_dic(cd_path)
    cd_sig2id_dic = dict(zip(cd_id2sig_dic.values(), cd_id2sig_dic.keys()))
    used_cd_dic = {}
    ac_save_file = open(ac_save_path, 'w')
    write_line_count = 0
    ac_sum = 0.0
    ac_size = 0
    for sstp_id, ss, tp in sstp_itr:
        ac_value = alpha * float(ss) + beta * float(tp)
        if gamma > 0:
            cd_value = find_v_by_sharp_k(sharp_key_pair = sstp_id,
                                         key_id_dic = sstp_id_dic,
                                         cd_dic = cd_dic, cd_sig2id_dic = cd_sig2id_dic, used_cd_dic = used_cd_dic)
            ac_value += gamma * cd_value
        ac_sum += ac_value
        ac_save_file.write('{}{}{}{}'.format(sstp_id, common.csv_splitor, ac_value, common.linesep))
        write_line_count += 1
        ac_size += 1
        if write_line_count >= common.flush_size:
            ac_save_file.flush()
            write_line_count = 0
    ac_save_file.close()

    cd_dic_not_used_num = len(cd_dic) - len(used_cd_dic)
    if cd_dic_not_used_num > 0 and gamma > 0:
        print('total cd_dic num: %d ; cd_dic not used num: %d ' % (len(cd_dic), cd_dic_not_used_num))
    print("ac size: %d" % ac_size)
    avg_ac = float(ac_sum / ac_size)
    print("average augmentation coefficient is %f" % avg_ac)
    return avg_ac


def method_augmentation(sstp_path, ac_save_path, avg_ac):
    id2vec_dic = load_csv_as_dic('{}.ss'.format(sstp_path))
    ac_itr = file_iterator(ac_save_path)
    result_dic = dict()
    for sstp_id, ac_value in ac_itr:
        if ac_value < avg_ac: continue
        id1, id2 = sstp_id.split(common.ss_key_splitor)
        # id1, id2 = int(ids[0]), int(ids[1])
        doc_vector1, doc_vector2 = id2vec_dic[id1], id2vec_dic[id2]
        doc_vector1 = np.fromstring(string = doc_vector1, sep = ',').reshape((-1, dim), order = 'C')
        doc_vector2 = np.fromstring(string = doc_vector2, sep = ',').reshape((-1, dim), order = 'C')
        if id1 not in result_dic:
            result_dic[id1] = doc_vector1 + ac_value * doc_vector2
        else:
            result_dic[id1] += ac_value * doc_vector2

        if id2 not in result_dic:
            result_dic[id2] = doc_vector2 + doc_vector1 * ac_value
        else:
            result_dic[id2] += doc_vector1 * ac_value

    id2vec_dic.update(result_dic)
    return id2vec_dic


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-ss", "--sstp_path", dest = "sstp_path", required = True)
    parser.add_argument("-cd", "--cd_path", dest = "cd_path", required = True)
    parser.add_argument("-c",  "--code_vector_dir", dest = "code_vector_dir", required = True)
    parser.add_argument("-ac", "--ac_save_path", dest = "ac_save_path", required = True)
    parser.add_argument("-s",  "--save_dir", dest = "save_dir", required = True)
    parser.add_argument("-b",  "--br_path", dest = "br_path", required = True)
    parser.add_argument("-i",  "--br_id", dest = "br_id",   required = True)
    parser.add_argument("-l",  "--link_buggy_path", dest = "link_buggy_path", required = True)
    parser.add_argument("-d",  "--dim", dest = "dim",     required = True)
    parser.add_argument("-e",  "--epochs",  dest = "epochs",  required = True)
    parser.add_argument("-alpha", "--alpha", dest = "alpha", required = True)
    parser.add_argument("-beta", "--beta", dest = "beta", required = True)
    parser.add_argument("-gamma", "--gamma", dest = "gamma", required = True)
    args = parser.parse_args()
    sstp_path, cd_path = args.sstp_path, args.cd_path
    code_vector_dir = args.code_vector_dir
    ac_save_path = args.ac_save_path
    br_path = args.br_path
    br_id = args.br_id
    link_buggy_path = args.link_buggy_path
    save_dir = args.save_dir
    dim = int(args.dim)
    epochs = int(args.epochs)
    alpha, beta, gamma = float(args.alpha), float(args.beta), float(args.gamma)

    start = time.process_time()
    print("Start to Calculate Query Expansion...")
    avg_ac = calculate_ac(sstp_path = sstp_path, cd_path = cd_path, ac_save_path = ac_save_path)

    id2vec_dic = method_augmentation(sstp_path = sstp_path, ac_save_path = ac_save_path, avg_ac = avg_ac)
    id2sig_dic = load_csv_as_dic(path = "{}.dic".format(sstp_path))

    # Rank
    br_vector = load_brv(file_path = br_path, dim = dim)
    rel_list = rank.cal_rel(br_vector, id2vec_dic)
    link_dic = rank.load_link_dic(link_buggy_path)
    buggy_method_list = link_dic[br_id]
    # 输出格式与iBug项目一致，则可以复用iBug计算TopK、MAP、MRR的代码
    # 输出格式： bug报告ID$真实标签$计算相关度$路径方法名
    result_list = ['{}${}${}${}'.format(br_id, x[1],
                                        (0, 1)[trim_method(trim_template_T(id2sig_dic[x[0]])) in buggy_method_list],
                                        trim_template_T(id2sig_dic[x[0]])) for x in rel_list]

    proj_id = br_id
    abrstr = '{}{}{}'.format(int(10 * alpha), int(10 * beta), int(10 * gamma))
    save_path = '{}/{}_{}_{}_{}'.format(save_dir, proj_id, dim, epochs, abrstr)
    with open(save_path, 'w') as f:
        f.write(common.linesep.join(result_list))

    elapsed = round(time.process_time() - start, 2)
    print("Finished Calculate Semantic Similarity. Time used : %.2f seconds" % elapsed)

    # import subprocess
    # subprocess.call(['./zou_cal_HitK-MAP-MRR.sh', save_path])
