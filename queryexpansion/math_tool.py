import numpy as np

# calculate average number in list
def average(list, size):
    return sum(list)/size


# sigmoid
def sigmoid(x):
    s = 1.0 / (1.0 + np.exp(-x))
    return s


# Calculate cosine similarity between two [line] vector
def cosine_similarity(vec1, vec2):
    l1 = np.linalg.norm(vec1)
    l2 = np.linalg.norm(vec2)
    if l1 == 0.0 or l2 == 0.0:
        return 0.0
    return float(np.dot(vec1, vec2.T) / (l1 * l2))
