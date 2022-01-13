import sys
import pandas as pd
from openpyxl import load_workbook


def excel_read(file_name):
    print("[Python - Excel Read] Start file_name:", file_name)

    xlsx = pd.read_excel("static/" + file_name,
                         header=None, skiprows=2, engine="openpyxl")

    print("[Python - Excel Read] Pandas Excel Read Success. test-datas", xlsx[7][0])


if __name__ == "__main__":
    excel_read(sys.argv[1])
