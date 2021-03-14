# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 17:06:21 2021

@author: choon
"""
from typing import List

from emvcomappinginfo import make_root_obj_id_map
from emvcospec import DataObject, extract_tag, ObjInfo
from crc import crc16iso13239

def parse_qr_code(toparse, template=make_root_obj_id_map(), recurse=True, add_info=False):
    dat_objs = []
    obj_map = template.get_obj_map(toparse)
    while len(toparse) > 4:
        tagid, length, payload, toparse = extract_tag(toparse)
        obj_info = obj_map.get(tagid, ObjInfo("tagid", "Unknown", length, -1, "O"))
        if obj_info.template and recurse:
            children = parse_qr_code(payload, obj_info.template, recurse=recurse, add_info=add_info)
        else:
            children = []
        if add_info:
            info = obj_info
        else:
            info = None
        dat_objs.append(DataObject(tagid, length, payload, children, info))
    return dat_objs

            
def print_parsed_info(
    data_objects: List[DataObject], 
):
    child_objs = []
    table = []
    for obj in data_objects:
        info = obj.info
        if info is None:
            print(obj)
        table.append((obj.tagid, info.name, obj.length, obj.payload))
        if obj.children:
            child_objs.append((obj))
    headers = ["Tag", "Name", "Length", "Payload"]
    try:
        import tabulate
        output_str = tabulate.tabulate(
            table, headers=headers
        )
    except (ImportError, NameError):
        print("`tabulate` not imported. Falling back to normal prints...")
        print("To get pretty printing, pip install tabulate")
        print("")
        output_str = "\t".join(headers) + "\n"
        output_str += "\n".join([x.__repr__() for x in table])
    
    print(output_str)
    if child_objs:
        for obj_with_children in child_objs:
            print("\nChild Objs for Tag {0}:".format(obj_with_children.tagid))
            print_parsed_info(obj_with_children.children)


def generate_qr_code(tags: List[DataObject], sort=False, add_crc=True):
    if sort:
        tags.sort(key=lambda x: x.tagid)
    output = []
    for tag in tags:
        # Do not add crc here, we do it outselves later
        if tag.tagid == "63":
            continue
        if not tag.children:
            payload = tag.payload
        else:
            payload = generate_qr_code(tag.children, sort=sort, add_crc=False)
        length = tag.length if tag.length > 0 else len(payload)
        output.append("{0}{1:02d}{2}".format(tag.tagid, length, payload))
    if add_crc:
        raw_output = "".join(output) + "6304"
        output = raw_output + crc16iso13239(raw_output)
    else:
        output = "".join(output)
    return output


class QRObject:
    def generate_tags(self):
        raise NotImplementedError("Not Implemented")


class EMVCOQR(QRObject):    
    def __init__(
        self,
        merchants: dict,    # {"tagid1": QRObject, "tagid2: QRObject2}
        merchant_category_code: str = "0000",
        transaction_currency: str = "702",
        transaction_amount: float = -1,
        tip_or_convenience_indicator: str = "",
        value_of_convenience_fee_fixed: str = "",
        value_of_convenience_fee_pct: str = "",
        country_code: str = "SG",
        merchant_name: str = "NA",
        merchant_city: str = "SINGAPORE",
        postal_code: str = ""
    ):
        
        # Some sane defaults
        self.merchants = merchants
        self.merchant_category_code = merchant_category_code
        self.transaction_currency = transaction_currency
        self.transaction_amount = transaction_amount
        self.tip_or_convenience_indicator = tip_or_convenience_indicator
        self.value_of_convenience_fee_fixed = value_of_convenience_fee_fixed
        self.value_of_convenience_fee_pct = value_of_convenience_fee_pct
        self.country_code = country_code
        self.merchant_name = merchant_name
        self.merchant_city = merchant_city
        self.postal_code = postal_code
        
    def generate_tags(
        self,
        merchants = None,
        merchant_category_code = None,
        transaction_currency = None,
        transaction_amount = None,
        tip_or_convenience_indicator = None,
        value_of_convenience_fee_fixed = None,
        value_of_convenience_fee_pct = None,
        country_code = None,
        merchant_name = None,
        merchant_city = None,
        postal_code = None,
    ):
        if merchants is None:
            merchants = self.merchants
        if merchant_category_code is None:
            merchant_category_code = self.merchant_category_code
        if transaction_currency is None:
            transaction_currency = self.transaction_currency
        if transaction_amount is None:
            transaction_amount = self.transaction_amount
        if tip_or_convenience_indicator is None:
            tip_or_convenience_indicator = self.tip_or_convenience_indicator
        if value_of_convenience_fee_fixed is None:
            value_of_convenience_fee_fixed = self.value_of_convenience_fee_fixed
        if value_of_convenience_fee_pct is None:
            value_of_convenience_fee_pct = self.value_of_convenience_fee_pct
        if country_code is None:
            country_code = self.country_code
        if merchant_name is None:
            merchant_name= self.merchant_name
        if merchant_city is None:
            merchant_city = self.merchant_city
        if postal_code is None:
            postal_code = self.postal_code        
    
        mandatory_tags = [
            DataObject("00", 2, "01"),
            DataObject("01", 2, "11"),          # Static QR 
            DataObject("52", payload=merchant_category_code),  # Merchant Category Code
            DataObject("53", payload=transaction_currency),
            DataObject("58", payload=country_code),
            DataObject("59", payload=merchant_name),
            DataObject("60", payload=merchant_city),            
        ]
    
        if merchants:
            for tagid, merchant in merchants.items():
                mandatory_tags.append(DataObject(tagid, children=merchant.generate_tags()))
        if transaction_amount > 0:
            mandatory_tags.append(DataObject("54", payload="{:.2f}".format(transaction_amount)))
        if tip_or_convenience_indicator:
            mandatory_tags.append(DataObject("55", payload=tip_or_convenience_indicator))
        if value_of_convenience_fee_fixed:
            mandatory_tags.append(DataObject("56", payload=value_of_convenience_fee_fixed))
        if value_of_convenience_fee_pct:
            mandatory_tags.append(DataObject("57", payload=value_of_convenience_fee_pct))
        if postal_code:
            mandatory_tags.append(DataObject("61", payload=postal_code))       
        return mandatory_tags