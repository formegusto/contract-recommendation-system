import math as mt
from numpy import dot
from numpy.linalg import norm
from scipy.stats import pearsonr


def euclidean_distance(A, B):
    err = 0
    length = len(A)
    for idx in range(0, length):
        tmp = ((A[idx] - B[idx]) ** 2)
        err += tmp

    return mt.sqrt(err)


def cosine_similarity(A, B):
    return dot(A, B) / (norm(A) * norm(B))


def corr(A, B):
    return pearsonr(A, B)[0]


def sumDiffer(A, B):
    length = len(A)
    err = 0
    for idx in range(0, length):
        err += ((A[idx] - B[idx]) ** 2)
    return mt.sqrt(err / length)


def improved_similarity(A, B, w):
    cos_sim = cosine_similarity(A, B)
    sum_diff = sumDiffer(A, B)
    w **= sum_diff

    return cos_sim * w
