# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 08:18:52 2021

@author: choon
"""

from emvospec import ObjInfo, repeated_obj_info


MASTERCARD_ACCOUNT_INFO_TEMPLATE = {
    "04": ObjInfo("04", "Mastercard ID", "N", -1, "M")
}

AMERICAN_EXPRESS_ACCOUNT_INFO_TEMPLATE = {
    "11": ObjInfo("11", "Amex ID 11", "N", -1, "O"),
    "12": ObjInfo("12", "Amex ID 12", "N", -1, "O"),
}

UNION_PAY_INTERNATIONAL_ACCOUNT_INFO_TEMPLATE = {
    "15": ObjInfo("15", "UPo ID", "N", -1, "O"),
}



MERCHANT_ACCOUNT_INFO_TEMPLATE = {
    "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "M"),
    **repeated_obj_info(ObjInfo("", "Payment network specific", "S", -1, "O"), 1, 100),
}



