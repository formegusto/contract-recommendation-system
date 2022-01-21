import pandas as pd
import numpy as np
from models import *
from utils.update_process import update_process


@update_process("bill-calc")
def bill_calc(peak_df, month_usage_df, min_per, max_per):
    analysis_df = month_usage_df.set_index("month")

    # 출력 데이터
    # 1. 계약별 유, 불리 가구 수
    better_comp_df = pd.DataFrame()
    better_single_df = pd.DataFrame()

    # 2. 계약별 아파트 전체 요금 변화
    bill_comp_df = pd.DataFrame()
    bill_single_df = pd.DataFrame()

    # 3. 계약별 공공설비사용요금 변화
    public_bill_comp_df = pd.DataFrame()
    public_bill_single_df = pd.DataFrame()

    for month in range(1, 13):
        # 1. 월별 사용량 데이터 파싱
        month_datas_df = pd.DataFrame(columns=["name", "usage (kWh)"])
        for idx in analysis_df.loc[month].index:
            household_name = idx
            household_kWh = analysis_df.loc[month][idx]

            month_datas_df = month_datas_df.append({
                "name": household_name,
                "usage (kWh)": household_kWh
            }, ignore_index=True)

        # Thinking
        # 세대부 전기는 정해져 있는데,
        # 공용부 전기는 정해져 있지가 않아서 입력되는 percentage에 따라, 변화하도록

        # 다음과 같은 공식을 사용할 수 있다.
        # n -> 공용부가 전체 APT에서 차지할 percentage
        # APT : households_kWh = 100 : (100 - n)
        # APT : public_kWh = 100 : n

        # 이에 따라,
        # APT = (households_kWh * 100) / (100 - n)
        # public_kwh = APT - households_kwh

        # 1. 계약별 유, 불리 가구 수
        better_comp_rows = np.array([])
        better_single_rows = np.array([])

        # 2. 계약별 아파트 전체 요금 변화
        bill_comp_rows = np.array([])
        bill_single_rows = np.array([])

        # 3. 계약별 공공설비사용요금 변화
        public_bill_comp_rows = np.array([])
        public_bill_single_rows = np.array([])

        for PUBLIC_PERCENTAGE in range(min_per, max_per + 1):
            households_kWh = sum(month_datas_df['usage (kWh)'].values)
            APT = round((households_kWh * 100) / (100 - PUBLIC_PERCENTAGE))
            public_kWh = round(APT - households_kWh)

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

            cnt = len(calc.households)
            comp_cnt = 0
            draw_cnt = 0
            single_cnt = 0

            # 1. 유불리 계산
            for idx in range(0, cnt):
                if calc.households[idx].bill > single_calc.households[idx].bill:
                    single_cnt += 1
                elif calc.households[idx].bill < single_calc.households[idx].bill:
                    comp_cnt += 1
                else:
                    draw_cnt

            better_comp_rows = np.append(better_comp_rows, comp_cnt)
            better_single_rows = np.append(better_single_rows, single_cnt)

            bill_comp_rows = np.append(bill_comp_rows, calc.bill)
            bill_single_rows = np.append(bill_single_rows, single_calc.bill)

            public_bill_comp_rows = np.append(
                public_bill_comp_rows, calc.public_bill)
            public_bill_single_rows = np.append(
                public_bill_single_rows, single_calc.public_bill)

        # 월 데이터 셋팅
        better_comp_df = better_comp_df.append(
            pd.Series(better_comp_rows, index=["{}".format(_) for _ in range(min_per, max_per + 1)], name=month))
        better_single_df = better_single_df.append(
            pd.Series(better_single_rows, index=["{}".format(_) for _ in range(min_per, max_per + 1)], name=month))

        bill_comp_df = bill_comp_df.append(
            pd.Series(bill_comp_rows, index=["{}".format(
                _) for _ in range(min_per, max_per + 1)], name=month)
        )
        bill_single_df = bill_single_df.append(
            pd.Series(bill_single_rows, index=["{}".format(
                _) for _ in range(min_per, max_per + 1)], name=month)
        )

        public_bill_comp_df = public_bill_comp_df.append(
            pd.Series(public_bill_comp_rows, index=["{}".format(
                _) for _ in range(min_per, max_per + 1)], name=month)
        )
        public_bill_single_df = public_bill_single_df.append(
            pd.Series(public_bill_single_rows, index=["{}".format(
                _) for _ in range(min_per, max_per + 1)], name=month)
        )

    return {
        "better": {
            "comp": better_comp_df,
            "single": better_single_df
        },
        "bill": {
            "comp": bill_comp_df,
            "single": bill_single_df
        },
        "public_bill": {
            "comp": public_bill_comp_df,
            "single": public_bill_single_df
        }
    }
