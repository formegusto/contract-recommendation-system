from modules.models import Household, Public
from modules.common import *
import math as mt


class ManagementOffice:
    def __init__(self,
                 month, peaks, households, APT,  # datas
                 contract,
                 general_fee_info=None):
        self.peaks = peaks
        self.APT = APT

        self.contract = contract
        self.select_fee(month, contract, general_fee_info)

        if contract == "종합계약":
            # 가구 객체화
            # - 가구별 지정된 계약에 요금들이 계산되도록 Property 구성해놨음.
            self.households = list()
            for idx in households.index:
                self.households.append(
                    Household(
                        name=households.iloc[idx]['name'],
                        kwh=households.iloc[idx]['usage (kWh)'],
                        contract=self.fee[0],
                        contract_name=contract
                    )
                )

            # 공용설비사용요금
            households_kwh = sum([_.kwh for _ in self.households])
            public_kwh = APT - households_kwh
            max_peak = peaks['peak (kW)'].max()
            charge_applied = max_peak * (public_kwh / APT)

            self.public = Public(
                kwh=public_kwh,
                charge_applied=charge_applied,
                contract=self.fee[1]
            )
            self.public_bill = self.public.elec_bill_vat_fund

            # 가구별 청구서 셋팅
            public_fee = round(self.public_bill /
                               len(self.households) / 10) * 10

            for household in self.households:
                household.set_bill(
                    public_fee=public_fee
                )

            # 아파트 청구서 셋팅
            bill = 0
            for household in self.households:
                bill += household.bill
            self.bill = bill
        elif contract == "단일계약":
            # 전체를 하나의 가구 본 상태에서 계약대로 계산식 진행
            # 후에 * len(household) 를 통해 아파트 전체 요금 통지서 확보
            num_household = len(households)
            mean_kwh = APT / num_household

            apart = Household(
                name="아파트",
                kwh=mean_kwh,
                contract=self.fee,
                contract_name=contract
            )
            basic = apart.basic * num_household
            elec_rate = apart.elec_rate * num_household
            env = apart.env * num_household
            fuel = apart.fuel * num_household

            elec_bill = basic + elec_rate + env - fuel
            self.bill = mt.floor((elec_bill
                                  + round(elec_bill * 0.1)
                                  + mt.floor(elec_bill * 0.037 * 0.1) * 10) * 0.1) * 10

            # 가구 객체화
            # - 가구별 지정된 계약에 요금들이 계산되도록 Property 구성해놨음.
            self.households = list()
            for idx in households.index:
                self.households.append(
                    Household(
                        name=households.iloc[idx]['name'],
                        kwh=households.iloc[idx]['usage (kWh)'],
                        contract=self.fee,
                        contract_name=contract
                    )
                )

            # 공공설비사용요금
            households_bill = sum(
                [_.elec_bill_vat_fund for _ in self.households]
            )
            self.public_bill = self.bill - households_bill

            # 가구별 청구서 셋팅
            public_fee = round(self.public_bill / len(self.households))
            for household in self.households:
                household.set_bill(
                    public_fee=public_fee
                )

    # 요금제 셋팅 메서드
    def select_fee(self, month, contract, general_fee_info):
        if contract == "종합계약":
            household_fee = None
            public_fee = None
            if (month >= 1 and month <= 6) or\
                    (month >= 9 and month <= 12):
                household_fee = low_pressure_fee
            else:
                household_fee = low_pressure_fee_summer

            if general_fee_info == None:
                raise Exception("종합계약은 일반용 전력 정보를 포함해야 합니다.\n")

            tmp_general_fee = None
            if general_fee_info == "저압":
                tmp_general_fee = general_fee[general_fee_info]
            elif len(general_fee_info) == 2:
                tmp_general_fee = general_fee[general_fee_info[0]]
                tmp_general_fee = tmp_general_fee[general_fee_info[1] - 1]
            else:
                raise Exception("일반용 전력 설정이 올바르지 않습니다\n"
                                + "저압, [고압 A, 0 or 1], [고압 B, 0 or 1]")

            if month >= 6 and month <= 8:
                public_fee = [tmp_general_fee[0], tmp_general_fee[1]]
            elif (month >= 3 and month <= 5) or\
                    (month >= 9 and month <= 10):
                public_fee = [tmp_general_fee[0], tmp_general_fee[2]]
            elif (month >= 1 and month <= 2) or\
                    (month >= 11 and month <= 12):
                public_fee = [tmp_general_fee[0], tmp_general_fee[3]]
            self.fee = [household_fee, public_fee]

        elif contract == "단일계약":
            if (month >= 1 and month <= 6) or\
                    (month >= 9 and month <= 12):
                self.fee = high_pressure_fee
            else:
                self.fee = high_pressure_fee_summer

        # print("[관리사무소] 계약 정보 셋팅 완료\n")
        # print(self.fee)
        # print("")
