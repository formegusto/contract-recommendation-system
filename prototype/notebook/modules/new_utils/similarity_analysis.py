import pandas as pd
import numpy as np
from modules.new_utils import bill_calc, normal_analysis, improved_similarity, aps
from sklearn.decomposition import TruncatedSVD


def get_reco_idx(month_usage_df):
    a = month_usage_df.set_index("month")
    a = np.array(a)
    r, c = a.shape
    imp_weight = 0.99

    recos = np.array([])
    for t in range(0, c - 1):
        if t == 0:
            dr_matrix = a
        else:
            dr_size = c - t
            svd = TruncatedSVD(n_components=dr_size)
            dr_matrix = svd.fit_transform(a)

        imp = np.array([])
        for A in dr_matrix:
            _ = np.array([])
            for B in dr_matrix:
                _ = np.append(_, improved_similarity(
                    A, B, imp_weight
                ))
            imp = np.append(imp, _)
            imp = imp.reshape(r, -1)

        reco_idx = imp.mean(axis=1).argmax()

        if ~np.any(recos == reco_idx):
            recos = np.append(recos, reco_idx)

    return recos


def similarity_analysis(month_usage_df, peak_df, min_per, max_per, db_processing=False):
    recos = get_reco_idx(month_usage_df)
    analysis_targets = month_usage_df.set_index(
        "month").iloc[recos].copy()
    mean_df = pd.DataFrame(analysis_targets.mean(axis=0).round()).T

    mean_df['month'] = 1

    bc_result = bill_calc(mean_df, peak_df, min_per, max_per)
    na_result = normal_analysis(bc_result)

    result = (bc_result, na_result)
    if db_processing:
        return aps((bc_result, na_result))

    return bc_result, na_result
