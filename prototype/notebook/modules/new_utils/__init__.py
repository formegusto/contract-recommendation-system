from modules.new_utils.bill_calc import bill_calc
from modules.new_utils.normal_analysis import normal_analysis
from modules.new_utils.mean_analysis import mean_analysis
from modules.new_utils.similarity_analysis import *
from modules.new_utils.similarity_calc import *
from modules.new_utils.load_excel import load_excel
from modules.new_utils.data_preprocessing import data_preprocessing
from modules.new_utils.analysis_processing import analysis_processing_single as aps

__all__ = ['bill_calc', 'normal_analysis',
           'mean_analysis', 'similarity_analysis', 'get_reco_idx',
           'euclidean_distance', 'cosine_similarity', 'corr', 'sumDiffer',
           'improved_similarity', 'load_excel', 'data_preprocessing', 'aps']
__version__ = "0.1.5"
