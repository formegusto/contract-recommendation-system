from utils import *
import sys
import requests as req


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
    result = bill_calc(p, m, min_per, max_per)

    analysis_result = analysis(result)
