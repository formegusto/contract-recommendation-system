import pandas as pd
from modules.new_utils import *


def mean_analysis(month_usage_df, peak_df, min_per, max_per):
    analysis_targets = month_usage_df.set_index("month").copy()
    mean_df = pd.DataFrame(analysis_targets.mean().round()).T

    mean_df['month'] = 1

    bc_result = bill_calc(mean_df, peak_df, min_per, max_per)
    na_result = normal_analysis(bc_result)

    return bc_result, na_result
