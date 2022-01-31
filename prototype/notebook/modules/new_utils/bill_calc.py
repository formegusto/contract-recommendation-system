import pandas as pd
import numpy as np
from modules.models import *


def bill_calc(month_usage_df, peak_df, min_per, max_per):
    analysis_df = month_usage_df.set_index("month")

    # 출력 데이터
    # 1. household_bill [DataFrame] month sort
    # - 가구별 개인 청구서
    # - numpy array 가 DataFrame을 numpy 화 시켜서 합쳐버리는 현상이 있음
    household_comp_bill = list()
    household_single_bill = list()

    # 2. bill DataFrame
    # - 아파트 전체 청구서
    comp_bill = pd.DataFrame()
    single_bill = pd.DataFrame()

    # 3. public_bill DataFrame
    # - 공동설비사용요금 청구서
    public_comp_bill = pd.DataFrame()
    public_single_bill = pd.DataFrame()

    # 4. 정보 : 가구 수, 표준편차, 평균, 변동계수
    information = list()

    for month in analysis_df.index:
        print("{} 월 계산 진행 합니다.".format(month))

        # 1. 월별 사용량 데이터 파싱
        month_datas_df = pd.DataFrame(columns=["name", "usage (kWh)"])
        household_names = np.array([])
        for idx in analysis_df.loc[month].index:
            household_name = idx
            household_kWh = analysis_df.loc[month][idx]
            household_names = np.append(household_names, idx)

            month_datas_df = month_datas_df.append({
                "name": household_name,
                "usage (kWh)": household_kWh
            }, ignore_index=True)

        # 세대부 사용량 계산 저장용 변수
        households_kWh = sum(month_datas_df['usage (kWh)'].values)
        households_cnt = len(month_datas_df['usage (kWh)'].values)
        month_household_comp_bill = pd.DataFrame(columns=household_names)
        month_household_single_bill = pd.DataFrame(columns=household_names)

        # 아파트 전체 요금 저장용 변수
        bill_comp_rows = np.array([])
        bill_single_rows = np.array([])

        # 공동설비요금 저장용 변수
        public_bill_comp_rows = np.array([])
        public_bill_single_rows = np.array([])

        for PUBLIC_PERCENTAGE in range(min_per, max_per + 1):
            APT = round((households_kWh * 100) / (100 - PUBLIC_PERCENTAGE))

            # 종합계약
            calc = ManagementOffice(
                month=month,
                peaks=peak_df,
                households=month_datas_df,
                APT=APT,
                contract="종합계약",
                general_fee_info=['고압 A', 1]
            )

            # 단일계약
            single_calc = ManagementOffice(
                month=month,
                peaks=peak_df,
                households=month_datas_df,
                APT=APT,
                contract="단일계약"
            )

            # 가구 최종청구서 파싱
            comp_household_bill_rows = np.array([])
            single_household_bill_rows = np.array([])
            for idx in range(0, households_cnt):
                comp_household_bill_rows = np.append(
                    comp_household_bill_rows, calc.households[idx].bill)
                single_household_bill_rows = np.append(
                    single_household_bill_rows, single_calc.households[idx].bill)

            month_household_comp_bill.loc[PUBLIC_PERCENTAGE] = comp_household_bill_rows
            month_household_single_bill.loc[PUBLIC_PERCENTAGE] = single_household_bill_rows

            bill_comp_rows = np.append(bill_comp_rows, calc.bill)
            bill_single_rows = np.append(bill_single_rows, single_calc.bill)

            public_bill_comp_rows = np.append(
                public_bill_comp_rows, calc.public_bill)
            public_bill_single_rows = np.append(
                public_bill_single_rows, single_calc.public_bill)

        household_comp_bill.append(month_household_comp_bill)
        household_single_bill.append(month_household_single_bill)

        comp_bill = comp_bill.append(
            pd.Series(bill_comp_rows, index=["{}".format(
                _) for _ in range(min_per, max_per + 1)], name=month)
        )
        single_bill = single_bill.append(
            pd.Series(bill_single_rows, index=["{}".format(
                _) for _ in range(min_per, max_per + 1)], name=month)
        )

        public_comp_bill = public_comp_bill.append(
            pd.Series(public_bill_comp_rows, index=["{}".format(
                _) for _ in range(min_per, max_per + 1)], name=month)
        )
        public_single_bill = public_single_bill.append(
            pd.Series(public_bill_single_rows, index=["{}".format(
                _) for _ in range(min_per, max_per + 1)], name=month)
        )

        count = month_datas_df['usage (kWh)'].count()
        mean = round(month_datas_df['usage (kWh)'].mean())
        std = round(month_datas_df['usage (kWh)'].std())
        rsd = round(std/mean * 100)

        print("가구 수: {} / 평균: {} / 표준편차: {} / 변동계수: {}".format(count, mean, std, rsd))

        infos = {
            "count": count,
            "mean": mean,
            "std": std,
            "rsd": rsd
        }
        information.append(infos)

    return {
        "params": {
            "min_per": min_per,
            "max_per": max_per
        },
        "information": information,
        "households_bill": {
            "comp": household_comp_bill,
            "single": household_single_bill,
        },
        "bill": {
            "comp": comp_bill,
            "single": single_bill
        },
        "public_bill": {
            "comp": public_comp_bill,
            "single": public_single_bill
        }
    }
