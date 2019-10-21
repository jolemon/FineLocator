import numpy as np


# calculate average number in list
def average(list, size):

    import sys
    sys.setrecursionlimit(100000)

    if size == 1:
        return list[0]
    return average(list, size-1)*(size-1)/size + list[size-1]/size


# TODO
def max_pooling():
    return


# sigmoid函数
def sigmoid(x):
    s = 1 / (1 + np.exp(-x))
    return s


# TODO 正确性
def cal_cosine_similarity(vec_1, vec_2):
    vector_1 = np.mat(vec_1)
    vector_2 = np.mat(vec_2)
    num = float(vector_1 * vector_2.T)
    denom = np.linalg.norm(vector_1) * np.linalg.norm(vector_1)
    cos = num / denom
    return cos