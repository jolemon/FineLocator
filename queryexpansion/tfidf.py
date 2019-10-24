from collections import Counter
import math
from argparse import ArgumentParser
import os

# read doc from bugreport and code.
def load_bug_report(file_path, save_dic):
    file = open(file_path, 'r')
    lines = file.readlines()
    for line in lines:
        if line is not None:
            line = line.strip().split()
            save_dic[file_path] = Counter(line)
            break
    return save_dic


def load_code(proj_path, correspond_path, save_dic):
    for root, dirs, files in os.walk(proj_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file) 
                correspond_file_path = file_path.replace(proj_path, correspond_path)
                f = open(file_path, 'r')
                cf = open(correspond_file_path, 'r')
                lines = f.readlines()
                clines = cf.readlines()
                for j in range(len(lines)):
                    line = lines[j]
                    if line is not None:
                        line = line.replace('分', '')
                        line = line.strip().split()
                        method_signature = clines[j].split(',')[0]
                        key = file_path + '#' + method_signature
                        save_dic[key] = Counter(line)
                f.close()
    return save_dic


# function to calculate tfidf
# count可以通过countlist得到， word可以通过count得到
# count[word]可以得到每个单词的词频， sum(count.values())得到整个doc的单词总数
def tf(word, count):
    return math.log(count[word] / sum(count.values()) ) + 1


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
    parser.add_argument("-co", "--code_path", dest = "code_path", required = True)
    parser.add_argument("-cr", "--correspond_path", dest = "correspond_path", required = True)
    args = parser.parse_args() 
    bug_report_path = args.bug_report_path
    code_path = args.code_path
    correspond_path = args.correspond_path

    corpus_dic = {}

    corpus_dic = load_bug_report(file_path = bug_report_path, save_dic = corpus_dic)
    corpus_dic = load_code(proj_path = code_path, correspond_path = correspond_path, save_dic = corpus_dic)

    countlist = list(corpus_dic.values())

    for doc in corpus_dic:
        counter = corpus_dic[doc]
        print("Top words in document {}".format(doc))
        scores = {word: tfidf(word, counter, countlist) for word in counter}
        sorted_words = sorted(scores.items(), key = lambda x: x[1], reverse = True)
        for word, score in sorted_words[:]:
            print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))













