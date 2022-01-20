import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from modules.utils.similarity_calc import *


# setting mean datas
def set_mean(result):
    mean_result = dict()

    for key in result.keys():
        if type(result[key]) == dict:
            mean_result[key] = set_mean(result[key])
        else:
            mean_result[key] = np.round(result[key].mean(axis=0).values)

    return mean_result

# setting analysis datas
# 4차원까지 행렬분해로 추천된 예시 달


def get_analysis_pattern(target_df):
    matrix = np.array(target_df)
    r, c = matrix.shape
    norm_matrix = (matrix.flatten() - matrix.flatten().min()) / \
        (matrix.flatten().max() - matrix.flatten().min(axis=0))
    norm_matrix = norm_matrix.reshape(r, c)
    norm_matrix
    imp_weight = 0.99

    dr_size = c
    reco_df = pd.DataFrame(columns=['차원축소 사이즈', '추천 인덱스'])
    while dr_size >= 2:
        if dr_size == c:
            dr_matrix = norm_matrix
        else:
            SVD = TruncatedSVD(n_components=dr_size)
            dr_matrix = SVD.fit_transform(norm_matrix)

        imp = np.array([])
        for A in dr_matrix:
            _ = np.array([])
            for B in dr_matrix:
                _ = np.append(_, improved_similarity(
                    A, B, imp_weight
                ))
            imp = np.append(imp, _)
        imp = imp.reshape(r, -1)

        reco_idx = imp.mean(axis=0).argmax()

        reco_df = reco_df.append({
            "차원축소 사이즈": dr_size,
            "추천 인덱스": reco_idx
        }, ignore_index=True)
        dr_size -= 1

    recos = list(set(reco_df['추천 인덱스']))

    analysis_pattern = np.array([])
    for reco_idx in recos:
        analysis_pattern = np.append(analysis_pattern, matrix[reco_idx])
    analysis_pattern = analysis_pattern.reshape(-1, c)

    return np.round(analysis_pattern.mean(axis=0))


def set_analysis(result):
    anal_result = dict()
    for key in result.keys():
        if type(result[key]) == dict:
            anal_result[key] = set_analysis(result[key])
        else:
            anal_result[key] = get_analysis_pattern(result[key])

    return anal_result


def analysis(result):
    return {
        "mean": set_mean(result),
        "anaylsis": set_analysis(result)
    }
