import pandas as pd
import numpy as np

# 일반분석
# 기능
# - 유리가구 수 체크
# - 손실율 변화 체크
# - 각 카테고리별 유리 변경 시점 기록 (종합계약이 유리해지는 시점)
# -- 아파트 전체 청구서
# -- 공동설비사용 청구서
# -- 유리 가구 수
# -- 손실율


def get_analysis(bc_result, pos_cnt, loss_ratio):
    bill = bc_result['bill']
    public_bill = bc_result['public_bill']
    months = bill['comp'].index

    min_per = bc_result['params']['min_per']

    # 1. 아파트 전체 청구서
    bill_change_per = np.array([])
    for month in months:
        Cs = bill['comp'].loc[month].values
        Ss = bill['single'].loc[month].values

        for idx, c in enumerate(Cs):
            if Ss[idx] > c:
                bill_change_per = np.append(bill_change_per, idx + min_per)
                break
            if idx == (len(Cs) - 1):
                bill_change_per = np.append(bill_change_per, 101)

    # 2. 공동설비사용 요금
    public_bill_change_per = np.array([])
    for month in months:
        Cs = public_bill['comp'].loc[month].values
        Ss = public_bill['single'].loc[month].values

        for idx, c in enumerate(Cs):
            if Ss[idx] > c:
                public_bill_change_per = np.append(
                    public_bill_change_per, idx + min_per)
                break
            if idx == (len(Cs) - 1):
                public_bill_change_per = np.append(
                    public_bill_change_per, 101)

    # 3. 유리가구 수
    pos_cnt_change_per = np.array([])
    for month in months:
        Cs = pos_cnt['comp'].loc[month].values
        Ss = pos_cnt['single'].loc[month].values

        for idx, c in enumerate(Cs):
            if Ss[idx] < c:
                pos_cnt_change_per = np.append(
                    pos_cnt_change_per, idx + min_per)
                break
            if idx == (len(Cs) - 1):
                pos_cnt_change_per = np.append(
                    pos_cnt_change_per, 101)

    # 4. 손실율
    loss_ratio_change_per = np.array([])
    for month in months:
        Cs = loss_ratio['comp'].loc[month].values
        Ss = loss_ratio['single'].loc[month].values

        for idx, c in enumerate(Cs):
            if Ss[idx] > c:
                loss_ratio_change_per = np.append(
                    loss_ratio_change_per, idx + min_per)
                break
            if idx == (len(Cs) - 1):
                loss_ratio_change_per = np.append(
                    loss_ratio_change_per, 101)

    return bill_change_per, public_bill_change_per, pos_cnt_change_per, loss_ratio_change_per


def normal_analysis(bc_result):
    households_bill = bc_result['households_bill']

    # 1. 계약별 파싱
    comp_bill = households_bill['comp']
    single_bill = households_bill['single']

    household_comp_pos = pd.DataFrame()
    household_single_pos = pd.DataFrame()

    comp_loss_ratio = pd.DataFrame()
    single_loss_ratio = pd.DataFrame()

    for month_idx, c in enumerate(comp_bill):
        s = single_bill[month_idx]
        rows = c.index

        min_per = rows[0]
        max_per = rows[-1]

        comp_pos_rows = np.array([])
        single_pos_rows = np.array([])

        comp_loss_ratio_rows = np.array([])
        single_loss_ratio_rows = np.array([])

        for PUBLIC_PERCENTAGE in range(min_per, max_per + 1):
            c_bills = c.loc[PUBLIC_PERCENTAGE].values
            s_bills = s.loc[PUBLIC_PERCENTAGE].values

            comp_pos_count = 0
            single_pos_count = 0

            comp_loss_rows = np.array([])
            single_loss_rows = np.array([])

            for idx, c_bill in enumerate(c_bills):
                s_bill = s_bills[idx]

                if c_bill > s_bill:
                    single_pos_count += 1
                elif c_bill < s_bill:
                    comp_pos_count += 1

                comp_loss = round(c_bill / s_bill * 100)
                single_loss = round(s_bill / c_bill * 100)

                comp_loss_rows = np.append(
                    comp_loss_rows, comp_loss)
                single_loss_rows = np.append(
                    single_loss_rows, single_loss)

            comp_loss_mean = np.round(comp_loss_rows.mean())
            single_loss_mean = np.round(single_loss_rows.mean())

            comp_pos_rows = np.append(comp_pos_rows, comp_pos_count)
            single_pos_rows = np.append(single_pos_rows, single_pos_count)

            comp_loss_ratio_rows = np.append(
                comp_loss_ratio_rows, comp_loss_mean)
            single_loss_ratio_rows = np.append(
                single_loss_ratio_rows, single_loss_mean)

        household_comp_pos = household_comp_pos.append(pd.Series(
            comp_pos_rows, index=["{}".format(_) for _ in range(min_per, max_per + 1)], name=(month_idx + 1)))
        household_single_pos = household_single_pos.append(pd.Series(
            single_pos_rows, index=["{}".format(_) for _ in range(min_per, max_per + 1)], name=(month_idx + 1)))

        comp_loss_ratio = comp_loss_ratio.append(pd.Series(
            comp_loss_ratio_rows, index=["{}".format(_) for _ in range(min_per, max_per + 1)], name=(month_idx + 1)))
        single_loss_ratio = single_loss_ratio.append(pd.Series(
            single_loss_ratio_rows, index=["{}".format(_) for _ in range(min_per, max_per + 1)], name=(month_idx + 1)))

    pos_cnt = {
        "comp": household_comp_pos,
        "single": household_single_pos
    }

    loss_ratio = {
        "comp": comp_loss_ratio,
        "single": single_loss_ratio
    }
    bc, pc, pcc, lrc = get_analysis(bc_result, pos_cnt, loss_ratio)
    return {
        "positive_count": pos_cnt,
        "loss_ratio": loss_ratio,
        "pos_change_per": {
            "bill": bc,
            "public_bill": pc,
            "positive_count": pcc,
            "loss_ratio": lrc
        }
    }
