import pandas as pd

from utils.update_process import update_process


@update_process("read-excel")
def load_excel(filepath):
    xlsx = pd.read_excel("static/" + filepath, header=None,
                         skiprows=2, engine="openpyxl")

    return xlsx
