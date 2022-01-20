import pandas as pd


def load_excel(filepath):
    xlsx = pd.read_excel(filepath, header=None, skiprows=2, engine="openpyxl")

    return xlsx
