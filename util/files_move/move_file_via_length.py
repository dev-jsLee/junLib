# -*- coding: utf-8 -*-
import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.library.junLib import *

def process(folder_path=None, length:str='8', extension=None, move_contain_resource=False):
    if length and folder_path:
        move_files_to_subfolders(folder_path, int(length), extension, move_contain_resource=move_contain_resource)

def run(select='', folder_path='', length=None):
    if not select:
        print('1. parent folder\n2. folder')
    select = select or str(strip_quotes(input("Enter select process : ")))
    if select == '1':
        folder_path = folder_path or strip_quotes(input('Enter folder path: ')) 
        length = length or strip_quotes(input('Enter length match chars: '))
        remove_empty_folders(folder_path)
        subs = get_dir_sub_folder_path(folder_path)
        for i, sub in enumerate(subs):
            process(folder_path=sub, length=length)

    if select == '2':
        folder_path = folder_path or strip_quotes(input('Enter folder path: ')) 
        length = length or strip_quotes(input('Enter length match chars: '))
        remove_empty_folders(folder_path)
        process(folder_path=folder_path, length=length)

    # elif select == '3':
    #     file_path = strip_quotes(input('Enter file path: '))
    #     length = strip_quotes(input('Enter length match chars: '))
    #     process(file_path=file_path, length=length)

def run_for_speaker(select='1', folder_path='', length:int=None, extension=None): # type: ignore
    if not select:
        print('1. folder\n2. file')
    select = str(strip_quotes(input("Enter select process : "))) if not select else select
    if select == '1':
        if not folder_path:
            folder_path = strip_quotes(input('Enter folder path: ')) 
        if not length:
            length = strip_quotes(input('Enter length match chars: ')) # type: ignore
        remove_empty_folders(folder_path)
        process(folder_path=folder_path, length=str(length), move_contain_resource=True) # type: ignore
        process(folder_path=folder_path, length=str(length), extension='xml', move_contain_resource=True) # type: ignore
        process(folder_path=folder_path, length=str(length), extension='csv', move_contain_resource=True) # type: ignore

    elif select == '2':
        file_path = strip_quotes(input('Enter file path: '))
        length = strip_quotes(input('Enter length match chars: ')) # type: ignore
        # process(file_path=file_path, length=length, extension='mp4', move_contain_resource=True)
        process(file_path=file_path, length=str(length), move_contain_resource=True) # type: ignore
if __name__ == "__main__":
    # run_for_speaker()
    run()
