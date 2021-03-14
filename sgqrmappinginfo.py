# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 08:18:52 2021

@author: choon
"""

from emvcospec import ObjInfo, repeated_obj_info, Template
from emvcomappinginfo import make_root_obj_id_map


_DEFAULT_ACCOUNT_INFO_TEMPLATE = {
    "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "O"),  
}


_MASTERCARD_ACCOUNT_INFO_TEMPLATE = {
    "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "O"),
    "04": ObjInfo("04", "Mastercard ID", "N", -1, "M")
}

_AMERICAN_EXPRESS_ACCOUNT_INFO_TEMPLATE = {
    "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "O"),
    "11": ObjInfo("11", "Amex ID 11", "N", -1, "O"),
    "12": ObjInfo("12", "Amex ID 12", "N", -1, "O"),
}

_UNION_PAY_INTERNATIONAL_ACCOUNT_INFO_TEMPLATE = {
    "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "O"),
    "15": ObjInfo("15", "UPo ID", "N", -1, "O"),
}

_DASH_ACCOUNT_INFO_TEMPLATE = {
    "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "M"),
    "01": ObjInfo("01", "Merchant Account", "ans", -1, "O"),
}

_OCBC_P2P_ACCOUNT_INFO_TEMPLATE = {
    "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "M"),
    "01": ObjInfo("01", "Merchant Account", "ans", -1, "O")
}

_EZ_LINK_ACCOUNT_INFO_TEMPLATE = {
    "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "M"),
    "01": ObjInfo("01", "Merchant ID", "ans", -1, "O"),
    "02": ObjInfo("02", "SGQR Indicator"),
    "03": ObjInfo("03", "Offline Usage"),
    "04": ObjInfo("04", "Verification Code")
}

_GRAB_PAY_ACCOUNT_INFO_TEMPLATE = {
    "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "M"),
    "01": ObjInfo("01", "Merchant ID", "ans", -1, "O"),
}

_DBS_PAYLAH_ACCOUNT_INFO_TEMPLATE = {
    "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "M"),
    "01": ObjInfo("01", "QR Transaction Ref ID", "ans", -1, "O"),
    "02": ObjInfo("02", "QR ID")
}

_NETS_ACCOUNT_INFO_TEMPLATE = {
    "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "M"),
    "01": ObjInfo("01", "QR Meta Data", "ans", -1, "O"),
    "02": ObjInfo("02", "Merchant ID", "ans", -1, "O"),
    "03": ObjInfo("03", "Terminal ID", "ans", -1, "O"),
    "09": ObjInfo("09", "Transaction Amount Modifier", "ans", -1, "O"),
    "99": ObjInfo("99", "Signature", "ans", -1, "O"),
}

_WECHAT_PAY_ACCOUNT_INFO_TEMPLATE = {
    "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "M"),
    "01": ObjInfo("01", "Merchant Account", "ans", -1, "O"),
    "02": ObjInfo("02", "Terminal ID", "ans", -1, "O"),
}

_UOB_ACCOUNT_INFO_TEMPLATE = {
    "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "M"),
    "01": ObjInfo("01", "Merchant Account", "ans", -1, "O"),
}

_PAYNOW_ACCOUNT_INFO_TEMPLATE = {
    "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "M"),
    "01": ObjInfo("01", "Proxy Type", "N", 1, "M"),
    "02": ObjInfo("02", "Proxy Value", "ans", -1, "O"),
    "03": ObjInfo("03", "Editable txn amount indicator", "N", 1, "M"),
    "04": ObjInfo("04", "Reference", "ans", -1, "O"),
    "05": ObjInfo("05", "QR Expiry Date", "ans", -1, "O"),
}

SG_MERCHANT_ID_TEMPLATE = {
    "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "M"),
    "01": ObjInfo("01", "SGQR ID Number", "ans", -1, "O"),
    "02": ObjInfo("02", "Version", "ans", -1, "O"),
    "03": ObjInfo("03", "Postal Code", "ans", -1, "O"),
    "04": ObjInfo("04", "Level Number", "ans", -1, "O"),
    "05": ObjInfo("05", "Unit Number", "ans", -1, "O"),
    "06": ObjInfo("06", "Miscellaneous", "ans", -1, "O"),
    "07": ObjInfo("07", "New Revision Date", "ans", -1, "O"),
}

_SGQR_ACCOUNT_INFO_TEMPLATE = {
    "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "M"),
    **repeated_obj_info(ObjInfo("", "Payment network specific", "S", -1, "O"), 1, 100),
    "51": ObjInfo("51", "SG Merchant ID", "ans", -1, "O", SG_MERCHANT_ID_TEMPLATE),
}

SGQR_ACCOUNT_INFO_TEMPLATE_MAP = Template(
    {
        "SG.COM.DASH.WWW": Template(_DASH_ACCOUNT_INFO_TEMPLATE),
        "SG.COM.OCBC": Template(_OCBC_P2P_ACCOUNT_INFO_TEMPLATE),
        "SG.COM.EZLINK": Template(_EZ_LINK_ACCOUNT_INFO_TEMPLATE),
        "COM.GRAB": Template(_GRAB_PAY_ACCOUNT_INFO_TEMPLATE),
        "COM.DBS": Template(_DBS_PAYLAH_ACCOUNT_INFO_TEMPLATE),
        "SG.COM.NETS": Template(_NETS_ACCOUNT_INFO_TEMPLATE),
        "COM.QQ.WEIXIN.PAY": Template(_WECHAT_PAY_ACCOUNT_INFO_TEMPLATE),
        "SG.COM.UOB": Template(_UOB_ACCOUNT_INFO_TEMPLATE),
        "SG.PAYNOW": Template(_PAYNOW_ACCOUNT_INFO_TEMPLATE),
        "SG.SGQR": Template(_SGQR_ACCOUNT_INFO_TEMPLATE)
    },
    keyon = "guid",
    default_obj_id_map = _DEFAULT_ACCOUNT_INFO_TEMPLATE
)

def sgqr_root_obj_id_map():
    overridden_objs = {
        **repeated_obj_info(ObjInfo("", "Merchant Account Information", "ans", -1, "O", SGQR_ACCOUNT_INFO_TEMPLATE_MAP), 26, 52),
        "51": ObjInfo("51", "SG Merchant ID", "ans", -1, "O", Template(SG_MERCHANT_ID_TEMPLATE))
    }
    return make_root_obj_id_map(
        overridden_objs
    )
