# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 06:40:01 2021

@author: choon
"""
from typing import List

import tabulate

from emvcospec import DataObject, ROOT_OBJ_ID_MAP

example_qr_code = "0002010102111531480007024800070280007025499435326590011COM.REMOPAY0110200000033802040000030400010404000099020127330015SG.COM.DASH.WWW0110100210041328650017COM.QQ.WEIXIN.PAY0110100000033702040000030400010404000099020129720013sg.com.ezlink0114FMP-10000003380204SGQR0317NPL-0001-0000000004046AF951800007SG.SGQR01121809072DDA29020701.00010306058602040200050200060400000708201809155204000053037025802SG5909hisenyuan6009Singapore63044F90"
example_qr_code2 = "00020101021126380009SG.PAYNOW010100211+6584554295030115204000053037025802SG5902NA6009SINGAPORE630416D8"
# Decode tag by tag

toparse = example_qr_code

def extract_tag(toparse):
    assert len(toparse) > 4
    tagid = toparse[:2]
    length = int(toparse[2: 4])
    payload = toparse[4: 4+length]
    remainder = toparse[4+length:]
    return tagid, length, payload, remainder

def parse_one_level(toparse, obj_map=ROOT_OBJ_ID_MAP):
    dat_objs = []
    while len(toparse) > 4:
        tagid, length, payload, toparse = extract_tag(toparse)
        obj_info = obj_map[tagid]
        if obj_info.template:
            children = parse_one_level(payload, obj_info.template)
        else:
            children = []
        dat_objs.append(DataObject(tagid, length, payload, children))
    return dat_objs

def print_parsed_info(data_objects: List[DataObject]):
    child_objs = []
    table = []
    for obj in data_objects:
        info = ROOT_OBJ_ID_MAP[obj.tagid]
        table.append((obj.tagid, info.name, obj.length, obj.payload))
        if obj.children:
            child_objs.append(obj)
    output_str = tabulate.tabulate(
        table, headers=["Tag", "Name", "Length", "Payload"]
    )
    print(output_str)
    if child_objs:
        for obj_with_children in child_objs:
            print("\nChild Objs for Tag {0}:".format(obj_with_children.tagid))
            print_parsed_info(obj_with_children.children)

output = parse_one_level(example_qr_code)
output2 = parse_one_level(example_qr_code2)
                
#print("Tag 1")
#print_parsed_info(output)

print("Tag 2")
print_parsed_info(output2)