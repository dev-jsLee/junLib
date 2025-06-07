"""
유틸리티 모듈

이 모듈은 다양한 유틸리티 함수들을 제공합니다.
"""

from .bulk_change_ext import bulk_change_ext
from .convert_to_json import convert_to_json
from .delete_specific_ext import delete_specific_ext
from .folder_lift import lift_folders
from .remove_empty_folder import remove_empty_folders
from .timestamp_sorter import sort_files_by_timestamp

__all__ = [
    'bulk_change_ext',
    'convert_to_json',
    'delete_specific_ext',
    'lift_folders',
    'remove_empty_folders',
    'sort_files_by_timestamp'
]

# -*- coding: utf-8 -*-
# v231018
import os
import sys
current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)
_workplace_folder_path = current_directory

while(True):
    if os.path.basename(_workplace_folder_path) == '_workplace': break
    else:
        _workplace_folder_path = os.path.dirname(_workplace_folder_path)
        continue
source_code_path = os.path.dirname(_workplace_folder_path)
_gitlab_path = os.path.dirname(source_code_path)
root_folder_path = os.path.dirname(_gitlab_path)
sys.path.append(source_code_path)