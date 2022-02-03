from utils import *
import sys


@update_process("reco-process-start")
def start():
    return


if __name__ == "__main__":
    file_name = sys.argv[1]

    start()
    xlsx = load_excel(file_name)
    p, m = data_preprocessing(xlsx)

    min_per = 10
    max_per = 80
    bc_result = bill_calc(m, p, min_per, max_per)

    na_result = normal_analysis(bc_result)

    mean_result = mean_analysis(m, p, min_per, max_per)
    anal_result = similarity_analysis(m, p, min_per, max_per)
