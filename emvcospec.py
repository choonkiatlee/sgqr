# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 07:14:39 2021

@author: choon
"""

from typing import Dict, List
import dataclasses

@dataclasses.dataclass
class DataObject:
    tagid: str      # 2 digit numeric value
    length: int   # 2 digit numeric value
    payload: str  # min length of 1 character, max length of 99 chars
    children: List = dataclasses.field(default_factory=(lambda: []))
    
@dataclasses.dataclass    
class Template:
    obj_id_map: Dict = dataclasses.field(default_factory=(lambda: {}))
    
    def __bool__(self):
        return bool(self.obj_id_map)
    
@dataclasses.dataclass
class ObjInfo:
    tagid: str
    name: str
    format_: str = "ans"
    length: int = -1
    presence: str = "O"
    template: Dict = dataclasses.field(default_factory=(lambda: {}))
    
def repeated_obj_info(obj_info, from_id, to_id):
    return {
        "{:02d}".format(x): ObjInfo("{:02d}".format(x), obj_info.name, obj_info.format_, obj_info.length, obj_info.presence, obj_info.template)
        for x in range(from_id, to_id)
    }




