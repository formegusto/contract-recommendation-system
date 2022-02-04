import pandas as pd
import datetime as dt


def data_preprocessing(xlsx):
    date_df = xlsx[3:][xlsx.columns[1:6]].copy()
    household_df = xlsx[xlsx.columns[7:]]

    date_list = [dt.datetime(
        date_df.loc[_][1],
        date_df.loc[_][2],
        date_df.loc[_][3],
        date_df.loc[_][4],
        date_df.loc[_][5]
    ) for _ in date_df.index]

    datas_df = pd.DataFrame(columns=['date'])
    datas_df['date'] = date_list

    for col in household_df:
        household_name = "{}-{}-{}".format(
            household_df[col][0],
            household_df[col][1],
            household_df[col][2]
        )
        datas_df[household_name] = household_df[col][3:].to_list()

    datas_df = datas_df.replace("-", 0)

    sum_df = pd.DataFrame(columns=['date', 'kWh', 'kW'])
    sum_df['date'] = date_list
    sum_df['kWh'] = [round(_) for _ in datas_df[datas_df.columns.difference(
        ['date'])].sum(axis=1).to_list()]
    sum_df['kW'] = (sum_df['kWh'] / 0.25).to_list()

    peak_df = pd.DataFrame(columns=['month', 'peak (kW)'])
    for month in range(1, 13):
        peak_df = peak_df.append({
            "month": str(month),
            "peak (kW)": sum_df[sum_df['date'].dt.month == month]['kW'].max()
        }, ignore_index=True)

    month_usage_df = pd.DataFrame(columns=['month'])
    month_usage_df['month'] = [_ for _ in range(1, 13)]

    for name in datas_df[datas_df.columns.difference(['date'])]:
        self_household_df = datas_df[['date', name]].copy()

        month_usage_df[name] = [
            round(
                self_household_df[self_household_df['date'].dt.month == month][name].sum())
            for month in range(1, 13)
        ]

    return (
        peak_df,
        month_usage_df
    )
