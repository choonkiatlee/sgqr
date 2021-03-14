# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 07:14:39 2021

@author: choon
"""

from typing import Dict, List, Optional
import dataclasses
    
@dataclasses.dataclass    
class Template:
    obj_id_map: Dict = dataclasses.field(default_factory=(lambda: {}))
    keyon: str = "id"   # "id" or "guid" (tag = 00)
    default_obj_id_map: Dict = dataclasses.field(default_factory=(lambda: {}))
    
    def __bool__(self):
        return bool(self.obj_id_map)
    
    def get_obj_map(self, toparse):
        if self.keyon == "id":
            return self.obj_id_map
        elif self.keyon == "guid":
            guid = get_payload_format_indicator(toparse).upper()
            if guid in self.obj_id_map:
                return self.obj_id_map[guid].obj_id_map
            else:
                return self.default_obj_id_map
        else:
            raise ValueError("unsupported keyon type")
        
        
@dataclasses.dataclass
class ObjInfo:
    tagid: str
    name: str
    format_: str = "ans"
    length: int = -1
    presence: str = "O"
    template: Template = dataclasses.field(default_factory=(lambda: Template()))
    
    
@dataclasses.dataclass
class DataObject:
    tagid: str         # 2 digit numeric value
    length: int = -1   # 2 digit numeric value
    payload: str = ""  # min length of 1 character, max length of 99 chars
    children: List = dataclasses.field(default_factory=(lambda: []))
    info: Optional[ObjInfo] = None
    

def repeated_obj_info(obj_info, from_id, to_id):
    return {
        "{:02d}".format(x): ObjInfo("{:02d}".format(x), obj_info.name, obj_info.format_, obj_info.length, obj_info.presence, obj_info.template)
        for x in range(from_id, to_id)
    }

def extract_tag(toparse):
    assert len(toparse) > 4
    tagid = toparse[:2]
    length = int(toparse[2: 4])
    payload = toparse[4: 4+length]
    remainder = toparse[4+length:]
    return tagid, length, payload, remainder

def get_payload_format_indicator(toparse):
    tagid = "-1"
    while len(toparse) > 4:
        tagid, length, payload, toparse = extract_tag(toparse)
        if tagid == "00":
            return payload
    raise ValueError("Could not find tag with id 00")


