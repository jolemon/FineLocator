import math
import math_tool

alpha = 0.8
beta = 0.1
gamma = 0.1

average_time_difference = 0
average_shortest_length = 0
average_augmentation_coefficient = 0


# TODO 统计word在词袋bow中出现的次数
def cal_word_frequency(word, bow):
    return 0


# TODO |M| : 代表项目中所有的方法数
def cal_num_of_methods():
    return 0


# TODO 统计项目中包含word的方法数
def cal_num_of_methods_containing_word(word):
    return 0


# The term frequency
def tf(word, bow):
    word_frequency = cal_word_frequency(word = word, bow = bow)
    return math.log(word_frequency) + 1


# the inverse document frequency
def idf(word):
    big_m = cal_num_of_methods()
    n_wj = cal_num_of_methods_containing_word(word)
    return math.log(big_m / n_wj)


def cal_tfidf(word, bow):
    return tf(word, bow) * idf(word)


# TODO
def cal_vector_multiply_tfidf(word, vector_for_word, bow):
    tfidf_for_word = cal_tfidf(word, bow)
    # vector_for_word是什么类型，如何乘以一个浮点数
    # vector_for_word.multiply(tfidf_for_word)
    return 0


# TODO 在方法级别上计算doc
def cal_doc_vector():
    # for all word in method : do cal_vector_multiply_tfidf() and get vec_tfidf_list
    # return max_pooling(vec_tfidf_list)
    return


# TODO 计算方法之间的平均修改长度
def cal_average_time_difference():
    return 0


def semantic_similarity(doc_1, doc_2):
    return math_tool.cal_cosine_similarity(vec_1 = doc_1, vec_2 = doc_2)


def temporal_proximity(last_modified_time_for_m1, last_modified_time_for_m2):
    time_diff = abs(last_modified_time_for_m1 - last_modified_time_for_m2)
    return math_tool.sigmoid(time_diff / average_time_difference)


def cal_average_shortest_length():
    return 0


# TODO JavaUnderstand. 两个方法之间是否有依赖关系，无则返回0，有则返回最短调用长度lp
def find_link_for_methods(method_1, method_2):
    return 0


def call_dependency(method_1, method_2):
    lp = find_link_for_methods(method_1 = method_1, method_2 = method_2)
    if lp == 0:
        return 0
    else:
        return math_tool.sigmoid(1-lp/average_shortest_length)


# TODO 是否需要定义类表示method，method包含其doc_vector, last_modify_time, 但还要另外计算call_dependency
def augmentation_coefficient(method_1, method_2):
    # return alpha * semantic_similarity() + beta * temporal_proximity() + gamma * call_dependency()
    return


# TODO 计算平均值
def cal_average_augmentation_coefficient():
    return 0


# TODO 所有的方法扩展需要保存吗？如何保存
def method_augmentation():
    return


if __name__ == '__main__':

    # 定义 alpha, beta, gamma

    average_time_difference = cal_average_time_difference()
    average_shortest_length = cal_average_shortest_length()
    average_augmentation_coefficient = cal_average_augmentation_coefficient()



