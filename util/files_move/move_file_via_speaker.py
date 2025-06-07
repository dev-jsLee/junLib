# -*- coding: utf-8 -*-
import os
import sys
current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)
_workplace_folder_path = current_directory

while(True):
    if os.path.basename(_workplace_folder_path) == '_workplace':
        break
    else:
        _workplace_folder_path = os.path.dirname(_workplace_folder_path)
        continue
source_code_path = os.path.dirname(_workplace_folder_path)
_gitlab_path = os.path.dirname(source_code_path)
root_folder_path = os.path.dirname(_gitlab_path)
sys.path.append(source_code_path)
from _workplace.library.junLib import *

def run(folder_path=None):
    folder_path = folder_path or strip_quotes(input("Enter folder path : "))
    files = get_files_path_in_folder_at_all(folder_path)
    for i, file_path in enumerate(files):
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        if str(file_name).__contains__('-'):
            default_file_name, time_info, speaker = str(file_name).split('-')
            move_file_to_current_other_folder(file_path, speaker)

if __name__ == "__main__":
    run()