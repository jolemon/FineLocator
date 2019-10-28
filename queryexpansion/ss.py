# Semantic similarity
import numpy as np
import os
from argparse import ArgumentParser


# delete blank space, "[[    " from head and "]]" from tail
def trim_text(string):
    return string.strip().replace("[[    ", "").replace("]]", "")


# read one line from br file and parse this line to a vector in shape of (1, dim)
def load_brv(file_path, dim):
    with open(file_path, 'r') as f:
        vec_text = f.readline()
        trim_vec_text = trim_text(vec_text)
        arr = np.fromstring(string = trim_vec_text, sep = ',    ')
        vec = arr.reshape((-1, dim), order = 'C')
        return vec


def _load_single_cv(file_path, dim):
    dic = dict()
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for k in range(0, len(lines)-1, 2):
            signature = lines[k+1]
            signature = signature.strip().replace("#", "").replace("分", "")
            # print(signature)
            vec_text = lines[k]
            trim_vec_text = trim_text(vec_text)
            arr = np.fromstring(string = trim_vec_text, sep = ',    ')
            vec = arr.reshape((-1, dim), order = 'C')
            dic[signature] = vec
        return dic


def load_cv(dir_path):
    files_dic = dict()
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                file_dic = _load_single_cv(file_path = file_path, dim = dim)
                files_dic[file_path] = file_dic
    return files_dic


# Calculate cosine similarity between two [line] vector
def cosine_similarity(vec1, vec2):
    return float(np.dot(vec1, vec2.T) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-c" , "--code_vector_dir", dest = "code_vector_dir", required = True)
    parser.add_argument("-br", "--br_vector_path" , dest = "br_vector_path" , required = True)
    parser.add_argument("-d" , "--dim"            , dest = "dim"            , required = True)

    args = parser.parse_args()
    code_vector_dir = args.code_vector_dir
    br_vector_path  = args.br_vector_path
    dim = int(args.dim)


    br_vec = load_brv(file_path = br_vector_path, dim = dim)
    files_dic = load_cv(dir_path = code_vector_dir)
    for file in files_dic:
        print(file)
        print(files_dic[file])
