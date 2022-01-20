from modules.utils.load_excel import load_excel
from modules.utils.data_preprocessing import data_preprocessing
from modules.utils.bill_calc import bill_calc
from modules.utils.analysis import analysis
from modules.utils.similarity_calc import *

__all__ = ['euclidean_distance', 'cosine_similarity', 'sumDiffer',
           'improved_similarity', 'load_excel', 'data_preprocessing', 'bill_calc', 'analysis']
__version__ = "0.1.0"
