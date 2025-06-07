# -*- coding: utf-8 -*-
import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.library.junLib import *

def process_yymmdd(yymmdd_folder_path):
    delete_folders_by_name(join_folder_path(yymmdd_folder_path, 'working'), 'speaker')
    # speaker_working_folder_path = join_folder_path(yymmdd_folder_path, 'working', 'speaker')
    # if path_exist(speaker_working_folder_path):
    #     files = get_files_path_at_all(speaker_working_folder_path)
    #     for i, file_path in enumerate(files):
    #         delete_file(file_path)
    #     remove_empty_folders(speaker_working_folder_path)

def run(select='', yymmdd_folder_path=None, file_path=None, yyyymm_folder_path=None, extension=None):
    extension = 'mp4'
    while(True):
        text_lines = []
        if not select:
            print('1. yyyymm/yymmdd folder')
            print('2. yyyymm folder')
            select = str(strip_quotes(input("Enter select process : "))) or '1'
        if select == '1':
            yymmdd_folder_path = yymmdd_folder_path or strip_quotes(input('Enter yymmdd_folder : '))
            process_yymmdd(yymmdd_folder_path)
            select = None

        elif select == '2':
            yyyymm_folder_path = yyyymm_folder_path or strip_quotes(input('Enter yyyymm_folder_path : '))
            yymmdd_folders = get_dir_sub_folder_path(yyyymm_folder_path)
            if yymmdd_folders:
                for i, yymmdd_folder_path in enumerate(yymmdd_folders, 1):
                    clear()
                    print(f"{i}/{len(yymmdd_folders)}")
                    process_yymmdd(yymmdd_folder_path)
            select = None
            yyyymm_folder_path = None
        else:
            select = None
            continue

if __name__ == "__main__":
    run()