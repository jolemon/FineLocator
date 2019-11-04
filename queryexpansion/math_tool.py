import numpy as np

# calculate average number in list
def average(list, size):
    import sys
    sys.setrecursionlimit(10000000)

    if size == 1:
        return list[0]
    return average(list, size-1)*(size-1)/size + list[size-1]/size


# sigmoid
def sigmoid(x):
    s = 1 / (1 + np.exp(-x))
    return s


# Calculate cosine similarity between two [line] vector
def cosine_similarity(vec1, vec2):
    return float(np.dot(vec1, vec2.T) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))