import math as mt
from modules.models.properties import *


class Household:
    env = env
    fuel = fuel
    vat = vat
    fund = fund
    elec_bill_vat_fund = elec_bill_vat_fund

    def __init__(self,
                 name, kwh, contract, contract_name):
        self.name = name
        self.kwh = kwh
        self.contract = contract
        self.contract_name = contract_name

    def set_bill(self,
                 public_fee):
        self.self_fee = self.elec_bill_vat_fund
        self.public_fee = public_fee
        self.bill = self.self_fee + self.public_fee

    @property
    def basic(self):
        fee = None
        for _ in self.contract:
            if _[0] <= self.kwh and _[1] >= self.kwh:
                fee = _[2]
                break
        return fee

    @property
    def elec_rate(self):
        kwh = self.kwh
        step = 0

        fee = 0
        for idx, _ in enumerate(self.contract):
            if (kwh + step) <= _[1]:
                fee += (kwh * _[3])
                break
            else:
                next_step = _[1]
                if idx == 0:
                    kwh -= _[1]
                    step += _[1]
                else:
                    prev = self.contract[idx-1]
                    next_step = (_[1] - prev[1])
                    kwh -= next_step
                    step += next_step
                fee += (next_step * _[3])

        return mt.floor(fee)

    @property
    def guarantee(self):
        if self.kwh <= 200:
            if self.contract_name == "종합계약":
                return 4000
            elif self.contract_name == "단일계약":
                return 2500
        else:
            return 0

    @property
    def elec_bill(self):
        bill = self.basic + self.elec_rate\
            - self.guarantee + self.env - self.fuel

        if bill < 1000:
            return 1000
        else:
            return bill
