# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from _workplace.library.junLib import *

def process(file_path):
    yymmdd_folder_path = parent_path(parent_path(file_path))
    yymmdd = os.path.basename(yymmdd_folder_path)
    yyyymm_folder_path = parent_path(yymmdd_folder_path)
    yyyymm = os.path.basename(yyyymm_folder_path)
    file_base_name = split_filename(basename(file_path))[0]

    text = f'\"{yymmdd}\",\"{file_base_name}.mp4\"'
    return text


def run(select='', folder_path=None, file_path=None, parent_folder_path=None, extension=None):
    extension = 'mp4'
    while(True):
        text_lines = []
        if not select:
            print('1. yymmdd folder')
            print('2. yyyymm folder')
            select = str(strip_quotes(input("Enter select process : ")))
            if not select:
                select = '1'
        if select == '1':
            if not folder_path:
                folder_path = strip_quotes(input('Enter folder path: '))
            if not extension:
                extension = strip_quotes(input('Enter target extension : '))
            folder = get_specific_sub_folder_path(folder_path, 'resource')
            files = get_files_path_in_folder_via_ext(folder, extension)
            if files:
                for i, file_path in enumerate(files):
                    process(file_path)
            select = None
            folder_path = None
                
        elif select == '2':
            if not parent_folder_path:
                parent_folder_path = strip_quotes(input('Enter parent folder path: '))
            folders = sub_path(parent_folder_path)
            if folders:
                for i, folder in enumerate(folders):
                    folder_path = get_specific_sub_folder_path(folder, 'resource')
                    files = get_files_path_in_folder_via_ext(folder_path, 'mp4')
                    for i, file_path in enumerate(files):
                        text = process(file_path)
                        text_lines.append(text)
                write_to_file(join_folder_path(parent_folder_path, os.path.basename(parent_folder_path)+'.csv'), text_lines)
            text_lines=None

            select = None
            parent_folder_path = None
        else:
            select = None
            continue

if __name__ == "__main__":
    run()