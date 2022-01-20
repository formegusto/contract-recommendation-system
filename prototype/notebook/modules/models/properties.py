import math as mt
from modules.common import env_fee, fuel_fee


@property
def env(self):
    return mt.floor(self.kwh * env_fee)


@property
def fuel(self):
    return mt.floor(self.kwh * fuel_fee)


@property
def vat(self):
    return round(self.elec_bill * 0.1)


@property
def fund(self):
    return mt.floor(self.elec_bill * 0.037 * 0.1) * 10


@property
def elec_bill_vat_fund(self):
    return mt.floor((self.elec_bill + self.vat + self.fund) * 0.1) * 10
