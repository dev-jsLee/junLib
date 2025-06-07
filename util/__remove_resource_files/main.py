# -*- coding: utf-8 -*-
import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.library.junLib import *

def process(file_path):
    yymmdd_folder_path = parent_path(parent_path(file_path))
    yymmdd = os.path.basename(yymmdd_folder_path)
    yyyymm_folder_path = parent_path(yymmdd_folder_path)
    yyyymm = os.path.basename(yyyymm_folder_path)
    file_base_name = os.path.splitext(os.path.basename(file_path))[0]

    text = f'\"{yyyymm}\",\"{file_base_name}.mp4\"'
    return text

def run(select='', yymmdd_folder=None, file_path=None, yyyymm_folder_path=None, extension=None):
    extension = 'mp4'
    while(True):
        text_lines = []
        if not select:
            print('1. yyyymm/yymmdd folder')
            print('2. yyyymm folder')
            select = str(strip_quotes(input("Enter select process : ")))
            if not select:
                select = '1'
        if select == '1':
            if not yymmdd_folder:
                yymmdd_folder = strip_quotes(input('Enter yymmdd_folder : '))
            if not extension:
                extension = strip_quotes(input('Enter target extension : '))
            resource_folder_path = get_specific_sub_folder_path(yymmdd_folder, 'resource')
            mp4_files = get_files_path_in_folder_via_ext(resource_folder_path, extension)
            if mp4_files:
                for i, file_path in enumerate(mp4_files):
                    delete_file(file_path)
            select = None
            resource_folder_path = None

        elif select == '2':
            yyyymm_folder_path = yyyymm_folder_path or strip_quotes(input('Enter yyyymm_folder_path : '))
            yymmdd_folders = get_dir_sub_folder_path(yyyymm_folder_path)
            if yymmdd_folders:
                for i, yymmdd_folder in enumerate(yymmdd_folders):
                    resource_folder_path = join_folder_path(yymmdd_folder, 'resource')
                    if path_exist(resource_folder_path):
                        mp4_files = get_files_path_in_folder_via_ext(resource_folder_path, 'mp4')
                        for i, file_path in enumerate(mp4_files):
                            delete_file(file_path)

            select = None
            yyyymm_folder_path = None
        else:
            select = None
            continue

if __name__ == "__main__":
    run()