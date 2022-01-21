import math as mt
from models.properties import *


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
        fee = 0
        for _ in self.contract:
            if kwh <= _[1]:
                fee += (kwh * _[3])
                break
            else:
                kwh -= _[1]
                fee += (_[1] * _[3])

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
