# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 08:19:18 2021

@author: choon
"""
from typing import Optional

from emvcospec import ObjInfo, repeated_obj_info, Template

_MERCHANT_ACCOUNT_INFO_TEMPLATE = Template(
    {
        "00": ObjInfo("00", "Globally Unique Identifier", "ans", -1, "M"),
        **repeated_obj_info(ObjInfo("", "Payment network specific", "S", -1, "O"), 1, 100),
    },
    "id"
)

def make_root_obj_id_map(
    objs_to_override: Optional[dict] = None,
    merchant_account_info_template: Template = _MERCHANT_ACCOUNT_INFO_TEMPLATE,
    additional_data_field_template: Optional[Template] = None,
    merchant_info_template: Optional[Template] = None,
) -> Template:
    if objs_to_override is None:
        objs_to_override = {}
    if additional_data_field_template is None:
        additional_data_field_template = Template()
    if merchant_info_template is None:
        merchant_info_template = Template()
    ROOT_OBJ_ID_MAP = {
        "00": ObjInfo("00", "Payload Format Indicator", "N", 2, "M"),
        "01": ObjInfo("01", "Point Of Initiation Method", "N", 2, "O"),
        **repeated_obj_info(ObjInfo("", "Merchant Account Information", "ans", -1, "M", merchant_account_info_template), 2, 52),
        "52": ObjInfo("52", "Merchant Category Code", "N", 4, "M"),
        "53": ObjInfo("53", "Transaction Currency", "N", 3, "M"),
        "54": ObjInfo("54", "Transaction Amount", "ans", -1, "C"),
        "55": ObjInfo("55", "Tip or Convenience Indicator", "N", 2, "O"),
        "56": ObjInfo("56", "Value Of Convenience Fee Fixed", "ans", -1, "C"),
        "57": ObjInfo("57", "Value Of Convenience Fee Percentage", "ans", -1, "C"),
        "58": ObjInfo("58", "Country Code", "ans", 2, "M"),
        "59": ObjInfo("59", "Merchant Name", "and", -1, "M"),
        "60": ObjInfo("60", "Merchant City", "ans", -1, "M"),
        "61": ObjInfo("61", "Postal Code", "ans", -1, "O"),
        "62": ObjInfo("62", "Additional Data Field Template", "S", -1, "O", additional_data_field_template),
        "64": ObjInfo("64", "Merchant Information -- Language Template", "S", -1, "O", merchant_info_template),
        "63": ObjInfo("63", "CRC", "ans", 4, "M"),
        **repeated_obj_info(ObjInfo("", "RFU For EMVCo", "S", -1, "O", {}), 65, 80),
        **repeated_obj_info(ObjInfo("", "Unreserved Templates", "S", -1, "O", {}), 80, 100),
        **objs_to_override,
    }
    return Template(ROOT_OBJ_ID_MAP, "id")
    
    