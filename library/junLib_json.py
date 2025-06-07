import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.library.junLib import *
import json

def write_to_json(json_data:dict, json_file_path, formatting:bool=True, sort:bool=False):
    with open(json_file_path, 'w') as json_file:
        json.dump(
            obj=json_data, 
            fp=json_file, 
            indent=(4 if formatting else None),
            sort_keys=sort,
            )

class json_controller():
    def __init__(self, json_data:dict=None, json_file_path:str=None) -> None: # type: ignore
        self.json_data = dict()
        self.json_file_path = json_file_path

    def set_json_data(self, json_data:dict):
        self.json_data = json_data
        return self
    
    def set_json_file_path(self, json_file_path):
        self.json_file_path = json_file_path
        return self

    def insert(self, target_dict:dict, new_key, new_value, index:int=-1):
        if index == -1: index = len(self.json_data)-1
        i = 0
        new_json_data = dict()
        for key, value in target_dict.items():
            if i == index:
                new_json_data[new_key] = new_value
            new_json_data[key] = value
            i += 1
        return new_json_data

    def insert_position(self, target_dict:dict, new_key, new_value, target_key:str, after:bool=True):
        i = 0
        new_json_data = dict()
        for key, value in target_dict.items():
            if not after and key == target_key:
                new_json_data[new_key] = new_value
            new_json_data[key] = value
            if after and key == target_key:
                new_json_data[new_key] = new_value
        return new_json_data
