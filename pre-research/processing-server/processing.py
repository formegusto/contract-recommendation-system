import pandas as pd
import datetime as dt


def read_excel(file_path):
    print(dt.datetime.now(), "read excel start :)")

    xlsx = pd.read_excel(
        "./static/" + file_path, header=None, skiprows=2, engine="openpyxl"
    )

    print(dt.datetime.now(), "read excel end :)")
