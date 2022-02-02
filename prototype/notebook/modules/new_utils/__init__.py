from modules.new_utils.bill_calc import bill_calc
from modules.new_utils.normal_analysis import normal_analysis
from modules.new_utils.mean_analysis import mean_analysis
from modules.new_utils.similarity_analysis import *
from modules.new_utils.similarity_calc import *

__all__ = ['bill_calc', 'normal_analysis',
           'mean_analysis', 'similarity_analysis', 'get_reco_idx',
           'euclidean_distance', 'cosine_similarity', 'corr', 'sumDiffer',
           'improved_similarity']
__version__ = "0.1.5"
