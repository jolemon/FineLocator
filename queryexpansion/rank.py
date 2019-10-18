import math_tool


def cal_rel(bug_report_vector, augmented_method_vector):
    return math_tool.cal_cosine_similarity(bug_report_vector, augmented_method_vector)


# 输出格式与iBug项目一致，则可以复用iBug计算TopK、MAP、MRR的代码
# 输出格式： bug报告ID$真实标签$计算相关度$路径方法名
