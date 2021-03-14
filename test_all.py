# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 15:17:25 2021

@author: choon
"""

from crc import crc16iso13239
import sgqrmappinginfo
import sgqr

example_qr_code = "0002010102111531480007024800070280007025499435326590011COM.REMOPAY0110200000033802040000030400010404000099020127330015SG.COM.DASH.WWW0110100210041328650017COM.QQ.WEIXIN.PAY0110100000033702040000030400010404000099020129720013sg.com.ezlink0114FMP-10000003380204SGQR0317NPL-0001-0000000004046AF951800007SG.SGQR01121809072DDA29020701.00010306058602040200050200060400000708201809155204000053037025802SG5909hisenyuan6009Singapore63044F90"
example_qr_code2 = "00020101021126380009SG.PAYNOW010100211+6584554295030115204000053037025802SG5902NA6009SINGAPORE630416D8"

def test_crc16():
    
    def check(example):
        tocrc = example[:-4]
        crc = example[-4:]
        assert crc == crc16iso13239(tocrc)
        
    check(example_qr_code)
    check(example_qr_code2)


def test_end_to_end():
    
    def check(example):
        sgqr_info = sgqrmappinginfo.sgqr_root_obj_id_map()
        parsed = sgqr.parse_one_level(example, sgqr_info, recurse=True, add_info=True)
        generated_code = sgqr.generate_code_from_tags(parsed, sort=False)
        assert generated_code == example
        
    check(example_qr_code)
    check(example_qr_code2)