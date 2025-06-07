# -*- coding: utf-8 -*-
import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.library.junLib import *

def remove_broadlist_mp4_files(yymmdd_folder_path=None):
    yymmdd_folder_path = yymmdd_folder_path or strip_quotes(input("Enter yymmdd folder path :"))
    yymmdd_string = os.path.basename(yymmdd_folder_path)
    video_folder_path = join_folder_path(yymmdd_folder_path, 'broadlist', f"{yymmdd_string}_video")
    mp4_files = get_files_path_in_folder_via_ext(video_folder_path, 'mp4')
    print("deleting")
    for i, mp4_file_path in enumerate(mp4_files):
        delete_file(mp4_file_path, False)
    print("delete done.")

def yyyymm_process(yyyymm_folder_path=None):
    yyyymm_folder_path = yyyymm_folder_path or strip_quotes(input("Enter yyyymm folder path :"))
    yymmdd_folders = get_dir_sub_folder_path(yyyymm_folder_path)
    yymmdd_folders = [f for f in yymmdd_folders if is_convertible_to_number(os.path.basename(f))]
    for i, yymmdd_folder_path in enumerate(yymmdd_folders, 1):
        clear()
        print(f"{i}\t{os.path.basename(yymmdd_folder_path)}")
        remove_broadlist_mp4_files(yymmdd_folder_path)

def select_process():
    print("1. yyyymm\n2. yymmdd")
    select = strip_quotes(input("Enter select(ex 1): ")) or '1'
    select = is_convertible_to_number(select, return_value=True)
    if select == 1:
        yyyymm_process()
    elif select == 2:
        remove_broadlist_mp4_files()
    print("done.")

if __name__ == "__main__":
    select_process()