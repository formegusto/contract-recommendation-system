import pandas as pd
import numpy as np
from modules.models import *


def bill_calc(month_usage_df, peak_df, min_per, max_per):

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

    comp_loss_ratio_df = pd.DataFrame()
    single_loss_ratio_df = pd.DataFrame()

    for month in analysis_df.index:
        print("{} 월 계산 진행 합니다.".format(month))
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
        APTs = np.array([])

        loss_ratio_comp_rows = np.array([])
        loss_ratio_single_rows = np.array([])

        # 4. percentage 별 comp, single 유리에 속해있는 가구
        positive_households = np.array([])

        # 5. 계약별 최소, 중간, 최대 가구 요금 기록
        min_value = month_datas_df[month_datas_df['usage (kWh)'] >= 100]['usage (kWh)'].values.min(
        )
        min_h_idx = np.abs(
            month_datas_df['usage (kWh)'].values - min_value).argmin()
        max_h_idx = month_datas_df['usage (kWh)'].values.argmax()
        mean = round(month_datas_df['usage (kWh)'].values.mean())
        mean_h_idx = np.abs(
            month_datas_df['usage (kWh)'].values - mean).argmin()

        min_kwh_info = {
            "comp": np.array([]),
            "single": np.array([])
        }
        mean_kwh_info = {
            "comp": np.array([]),
            "single": np.array([])
        }
        max_kwh_info = {
            "comp": np.array([]),
            "single": np.array([])
        }

        for PUBLIC_PERCENTAGE in range(min_per, max_per + 1):
            households_kWh = sum(month_datas_df['usage (kWh)'].values)
            APT = round((households_kWh * 100) / (100 - PUBLIC_PERCENTAGE))
            APTs = np.append(APTs, APT)
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

            comp_households = np.array([])
            single_households = np.array([])

            # 1. 유불리 계산
            # 2. 손실율 계산
            comp_loss_ratio = np.array([])
            single_loss_ratio = np.array([])
            for idx in range(0, cnt):
                comp_bill = calc.households[idx].bill
                single_bill = single_calc.households[idx].bill
                if idx == min_h_idx:
                    min_kwh_info = {
                        "comp": np.append(min_kwh_info['comp'], comp_bill),
                        "single": np.append(min_kwh_info['single'], single_bill)
                    }
                if idx == mean_h_idx:
                    mean_kwh_info = {
                        "comp": np.append(mean_kwh_info['comp'], comp_bill),
                        "single": np.append(mean_kwh_info['single'], single_bill)
                    }
                if idx == max_h_idx:
                    max_kwh_info = {
                        "comp": np.append(max_kwh_info['comp'], comp_bill),
                        "single": np.append(max_kwh_info['single'], single_bill)
                    }

                comp_loss_ratio = np.append(comp_loss_ratio,
                                            round(comp_bill / single_bill
                                                  * 100)
                                            )
                single_loss_ratio = np.append(single_loss_ratio,
                                              round(single_bill / comp_bill
                                                    * 100)
                                              )

                if comp_bill > single_bill:
                    single_cnt += 1
                    single_households = np.append(single_households, {
                        "name": calc.households[idx].name,
                        "kwh": calc.households[idx].kwh
                    })
                elif comp_bill < single_bill:
                    comp_cnt += 1
                    comp_households = np.append(comp_households, {
                        "name": calc.households[idx].name,
                        "kwh": calc.households[idx].kwh
                    })
                else:
                    draw_cnt += 1

            better_comp_rows = np.append(better_comp_rows, comp_cnt)
            better_single_rows = np.append(better_single_rows, single_cnt)

            bill_comp_rows = np.append(bill_comp_rows, calc.bill)
            bill_single_rows = np.append(bill_single_rows, single_calc.bill)

            loss_ratio_comp_rows = np.append(
                loss_ratio_comp_rows, round(comp_loss_ratio.mean()))
            loss_ratio_single_rows = np.append(
                loss_ratio_single_rows, round(single_loss_ratio.mean()))

            public_bill_comp_rows = np.append(
                public_bill_comp_rows, calc.public_bill)
            public_bill_single_rows = np.append(
                public_bill_single_rows, single_calc.public_bill)

            positive_households = np.append(positive_households, {
                "comp": comp_households,
                "single": single_households
            })

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

        comp_loss_ratio_df = comp_loss_ratio_df.append(
            pd.Series(loss_ratio_comp_rows, index=["{}".format(
                _) for _ in range(min_per, max_per + 1)], name=month)
        )
        single_loss_ratio_df = single_loss_ratio_df.append(
            pd.Series(loss_ratio_single_rows, index=["{}".format(
                _) for _ in range(min_per, max_per + 1)], name=month)
        )

    return {
        "information": {
            "apts": APTs,
            "positive_households": positive_households,
            "compare_households": {
                "min_household": min_kwh_info,
                "mean_household": mean_kwh_info,
                "max_household": max_kwh_info
            },
            "mean_hist": {

            }
        },
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
        },
        "loss_ratio": {
            "comp": comp_loss_ratio_df,
            "single": single_loss_ratio_df
        }
    }
