# -*- coding: utf-8 -*-
import os
import sys
from . import source_code_path
sys.path.append(source_code_path)
from _workplace.library.junLib import *

def run(folder_path=None, target_ext:str='csv'):
    speaker_root_folder_path = folder_path or strip_quotes(input("Enter folder path :"))
    taget_files = get_files_path_in_folder_via_ext(speaker_root_folder_path, target_ext)
    for i, target_file_path in enumerate(taget_files):
        default_file_name = os.path.splitext(os.path.basename(target_file_path))[0]
        family_files = get_files_path_in_folder_via_startwith(speaker_root_folder_path, default_file_name, 'mp4')
        for j, file_path in enumerate(family_files):
            xml_file_path = rename(file_path, new_extension='xml')
            move_file_to_current_other_folder(file_path, default_file_name)
            move_file_to_current_other_folder(xml_file_path, default_file_name)

if __name__ == "__main__":
    run()