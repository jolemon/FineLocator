from collections import Counter
import math
from argparse import ArgumentParser
import os

# read doc from bugreport and code.
def load_bug_report(file_path, save_dic):
    file = open(file_path, 'r')
    lines = file.readlines()
    total = ''
    for line in lines:
        line = line.strip()
        total += line
    save_dic[file_path] = Counter(total.split())
    return


def load_code(proj_path, correspond_path, save_dic):
    for root, dirs, files in os.walk(proj_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file) 
                correspond_file_path = file_path.replace(proj_path, correspond_path)
                rf = open(file_path, 'r')
                cf = open(correspond_file_path, 'r')
                lines = rf.readlines()
                clines = cf.readlines()
                for j in range(len(lines)):
                    try:
                        line = lines[j]
                        cline = clines[j]
                    except IndexError:
                        print('wrong in correspond file. please check!')
                        print('code path:', file_path)
                        print('correspond path:', correspond_file_path)
                        return
                    line = line.replace('分', '').strip()
                    if line is not None:
                        line = line.split()
                        method_signature = cline.split('$')[0]
                        key = file_path + '#' + method_signature
                        save_dic[key] = Counter(line)
                rf.close()
                cf.close()
    return


# function to calculate tfidf
# count可以通过countlist得到， word可以通过count得到
# count[word]可以得到每个单词的词频， sum(count.values())得到整个doc的单词总数
def tf(word, count):
    return math.log(count[word]) + 1
    # return math.log(count[word] / sum(count.values()) ) + 1


# 统计的是含有该单词的句子数
def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)


# len(count_list)是指句子的总数，n_containing(word, count_list)是指含有该单词的句子的总数，加1是为了防止分母为0
def idf(word, count_list):
    return math.log(len(count_list) / n_containing(word, count_list) )


# 将tf和idf相乘
def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)


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

    corpus_dic = {}

    load_bug_report(file_path = bug_report_path, save_dic = corpus_dic)
    load_code(proj_path = code_path, correspond_path = correspond_path, save_dic = corpus_dic)

    counter_list = list(corpus_dic.values())

    # save br
    if bug_report_path in corpus_dic:
        counter = corpus_dic[bug_report_path]
        pair = [str(word) + '$' + str(tfidf(word, counter, counter_list)) for word in counter]
        f = open(br_save_path, 'w')
        f.write('\n'.join(pair))
        f.close()
        print('finished calculate tfidf for br.')
        del corpus_dic[bug_report_path]

    # save method
    for doc in corpus_dic:
        doc_parts = doc.split('#')
        file_path = doc_parts[0]
        method = '#'.join(doc_parts[1:])
        write_path = file_path.replace(code_path, code_save_path)

        # create dirs
        write_dir = os.path.split(write_path)[0]
        if not os.path.isdir(write_dir):
            os.makedirs(write_dir)

        f = open(write_path, 'a')
        f.write(method + '分')
        counter = corpus_dic[doc]
        pair = [str(word) + '$' + str(tfidf(word, counter, counter_list) ) for word in counter]
        f.write('内'.join(pair))
        f.write('\n')
        f.close()

    print('finished calculate tfidf for method.')













