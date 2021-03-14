# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 06:40:01 2021

@author: choon
"""

from emvcospec import DataObject
import sgqr

example_qr_code = "00020101021126380009SG.PAYNOW010100211+6584554295030115204000053037025802SG5902NA6009SINGAPORE630416D8"

# 1) Parse the qr code into DataObjects
parsed_tags = sgqr.parse_qr_code(example_qr_code, recurse=True, add_info=True)

# 2) For debugging, print the obtained info from the tag
sgqr.print_parsed_info(parsed_tags)

# 3) Generate your own QR Code!
paynow_merchant = sgqr.PayNow(
    proxy_type = "mobile",
    proxy_value = "+6584554295",
    editable = True,
)
qr = sgqr.SGQR(
    sgqr_merchants=[paynow_merchant],
    transaction_amount=-1,
)
generated_code = sgqr.generate_qr_code(qr.generate_tags(), sort=True)

# 4) Check that they are the same
assert generated_code == example_qr_code

# 5) Alternatively for more control, specify the actual DataObjects yourself
tags = [
   DataObject("00", 2, "01"),
   DataObject("01", 2, "11"),
   DataObject("52", 4, "0000"),
   DataObject("53", 3, "702"),
#   DataObject("54", 2, "10"),
   DataObject("58", 2, "SG"),
   DataObject("59", 2, "NA"),
   DataObject("60", 9, "SINGAPORE"),
   DataObject("26", -1, "", children=[
       DataObject("00", 9, "SG.PAYNOW"),
       DataObject("01", 1, "0"),
       DataObject("02", 11, "+6584554295"),
       DataObject("03", 1, "1"),
   ])
]
generated_code_from_tags = sgqr.generate_qr_code(tags, sort=True)
assert generated_code_from_tags == example_qr_code   
   
# Just for the fun of it, lets look at the info contained in a slightly more involved qr code
example_qr_code2 = "0002010102111531480007024800070280007025499435326590011COM.REMOPAY0110200000033802040000030400010404000099020127330015SG.COM.DASH.WWW0110100210041328650017COM.QQ.WEIXIN.PAY0110100000033702040000030400010404000099020129720013sg.com.ezlink0114FMP-10000003380204SGQR0317NPL-0001-0000000004046AF951800007SG.SGQR01121809072DDA29020701.00010306058602040200050200060400000708201809155204000053037025802SG5909hisenyuan6009Singapore63044F90"

parsed_tags2 = sgqr.parse_qr_code(example_qr_code2, recurse=True, add_info=True)
print("")
print("***********************************************************")
print("")
sgqr.print_parsed_info(parsed_tags2)








