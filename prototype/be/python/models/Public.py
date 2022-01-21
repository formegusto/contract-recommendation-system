import math as mt
from models.properties import *


class Public:
    env = env
    fuel = fuel
    vat = vat
    fund = fund
    elec_bill_vat_fund = elec_bill_vat_fund

    def __init__(self,
                 kwh,
                 charge_applied,
                 contract):
        # 공용설비사용량
        self.kwh = kwh
        # 요금적용전력
        self.charge_applied = charge_applied
        self.contract = contract

    @property
    def basic(self):
        return mt.floor(self.charge_applied * self.contract[0])

    @property
    def elec_rate(self):
        return mt.floor(self.kwh * self.contract[1])

    @property
    def elec_bill(self):
        bill = self.basic + self.elec_rate + self.env - self.fuel

        if bill < 1000:
            return 1000
        else:
            return bill
