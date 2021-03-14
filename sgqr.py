# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 15:33:29 2021

@author: choon
"""

import datetime as dt
from typing import List, Union

import tabulate

from emvcomappinginfo import make_root_obj_id_map
from emvcospec import DataObject, extract_tag, ObjInfo
from crc import crc16iso13239

from emvcoqr import EMVCOQR, QRObject


from functools import partial
import sgqrmappinginfo
import emvcoqr

sgqr_info = sgqrmappinginfo.sgqr_root_obj_id_map()

parse_qr_code = partial(emvcoqr.parse_qr_code, template=sgqr_info)
print_parsed_info = emvcoqr.print_parsed_info
generate_qr_code = emvcoqr.generate_qr_code



class SGQR(emvcoqr.EMVCOQR):
    def __init__(self, sgqr_merchants, *args, **kwargs):
        super().__init__([], *args, **kwargs)
        self.sgqr_merchants = sgqr_merchants
    
    def generate_tags(self, sgqr_merchants = None, *args, **kwargs):
        if sgqr_merchants is None:
            sgqr_merchants = self.sgqr_merchants
        if sgqr_merchants:
            index = 26
            merchants = {}
            for merchant in sgqr_merchants:
                merchants["{:02d}".format(index)] = merchant
                index += 1
        return super().generate_tags(
            merchants = merchants,
            *args, **kwargs,
        )

class PayNow:
    def __init__(
        self, 
        editable: bool = False,
        proxy_type: str = "mobile",
        proxy_value: str = "",
        reference: str = "",
        qr_expiry_date: Union[str, dt.date] = "",
    ):
        self.editable = editable
        self.proxy_type = proxy_type
        self.proxy_value = proxy_value
        self.reference = reference
        self.qr_expiry_date = qr_expiry_date
    
    def generate_tags(
        self,
        editable = None,
        proxy_type = None,
        proxy_value = None,
        reference = None,
        qr_expiry_date = None,
    ):
        if editable is None:
            editable = self.editable
        if proxy_type is None:
            proxy_type = self.proxy_type
        if proxy_value is None:
            proxy_value = self.proxy_value
        if reference is None:
            reference = self.reference
        if qr_expiry_date is None:
            qr_expiry_date = self.qr_expiry_date
            
        if proxy_type == "mobile":
            proxy_type = "0"
        elif proxy_type == "uen":
            proxy_type = "2"
        else:
            raise ValueError("unsupported proxy_type")
        mandatory_outputs = [
            DataObject("00", payload="SG.PAYNOW"),
            DataObject("01", payload=proxy_type),
            DataObject("03", payload=("1" if editable else "0")),
        ]
        
        if proxy_value:
            mandatory_outputs.append(DataObject("02", payload=proxy_value))
        if reference:
            mandatory_outputs.append(DataObject("04", payload=reference))
        if qr_expiry_date:
            if isinstance(qr_expiry_date, dt.date):
                qr_expiry_date = qr_expiry_date.strftime("%y%m%d")  #YYMMDD
            mandatory_outputs.append(DataObject("05", payload=qr_expiry_date))
        return mandatory_outputs
