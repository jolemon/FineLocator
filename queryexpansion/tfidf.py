from collections import Counter
import math
from argparse import ArgumentParser
import os
import common


def load_bug_report(file_path: str):
    global corpus_dic
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        corpus_dic[file_path] = Counter(' '.join(lines).split())
    return


def load_code(proj_path: str, correspond_path: str):
    global corpus_dic
    for root, dirs, files in os.walk(proj_path):
        for file in files:
            if not file.endswith(common.java_file_postfix):
                continue

            file_path = os.path.join(root, file)
            correspond_file_path = file_path.replace(proj_path, correspond_path)
            rf, cf = open(file_path, 'r'), open(correspond_file_path, 'r')
            lines, clines = rf.readlines(), cf.readlines()
            rf.close()
            cf.close()
            if len(lines) != len(clines):
                print('wrong in correspond file. please check!')
                print('code path: %s' % file_path)
                print('correspond path: %s' % correspond_file_path)
                return
            for line, cline in zip(lines, clines):
                line = line.strip(common.afterPT_code_text_splitor).strip()
                cline_parts = cline.split(common.afterPT_code_correspond_splitor)
                if not line or not cline_parts:
                    continue
                key = "{}{}{}".format(file_path, common.path_sig_splitor, cline_parts[0])
                corpus_dic[key] = Counter(line.split())
    return


# count可以通过countlist得到， word可以通过count得到
# count[word]可以得到每个单词的词频， sum(count.values())得到整个doc的单词总数
def tf(word, count):
    return math.log(count[word]) + 1


# 统计的是含有该单词的句子数
def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)


# len(count_list)是指句子的总数，n_containing(word, count_list)是指含有该单词的句子的总数，加1是为了防止分母为0
def idf(word, count_list):
    return math.log(len(count_list) / n_containing(word, count_list))


# 将tf和idf相乘
def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)


corpus_dic = {}


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-br", "--bug_report_path", dest = "bug_report_path", required = True)
    parser.add_argument("-co", "--code_path",       dest = "code_path",       required = True)
    parser.add_argument("-cr", "--correspond_path", dest = "correspond_path", required = True)
    parser.add_argument("-bs", "--br_save_path",    dest = "br_save_path",    required = True)
    parser.add_argument("-cs", "--code_save_path",  dest = "code_save_path",  required = True)
    args = parser.parse_args() 
    bug_report_path = args.bug_report_path
    code_path = args.code_path
    correspond_path = args.correspond_path
    code_save_path = args.code_save_path
    br_save_path = args.br_save_path

    load_bug_report(file_path = bug_report_path)
    load_code(proj_path = code_path, correspond_path = correspond_path)

    counter_list = list(corpus_dic.values())

    # save br
    if bug_report_path not in corpus_dic:
        print('bug report not found!')
        exit(1)
    counter = corpus_dic[bug_report_path]
    pair = ['{}{}{}'.format(word, common.tfidfvalue_internal_splitor, tfidf(word, counter, counter_list)) for word in counter]
    with open(br_save_path, 'w') as f:
        f.write(common.linesep.join(pair))
    print('finished calculate tf-idf for br.')
    del corpus_dic[bug_report_path]

    # save method
    for doc in corpus_dic:
        doc_parts = doc.split(common.path_sig_splitor)
        file_path = doc_parts[0]
        method = common.path_sig_splitor.join(doc_parts[1:])  # 因为都是'#'
        write_path = file_path.replace(code_path, code_save_path)

        # create dirs
        write_dir = os.path.split(write_path)[0]
        if not os.path.isdir(write_dir):
            os.makedirs(write_dir)

        counter = corpus_dic[doc]
        with open(write_path, 'a') as f:
            f.write(method + common.method_tfidfvalue_splitor)
            pair = ['{}{}{}'.format(word, common.tfidfvalue_internal_splitor, tfidf(word, counter, counter_list)) for word in counter]
            f.write(common.tfidfvalue_external_splitor.join(pair))
            f.write(os.linesep)

    print('finished calculate tf-idf for method.')













