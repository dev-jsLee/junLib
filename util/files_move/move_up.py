# -*- coding: utf-8 -*-
import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.library.junLib import *

def run(select='', folder_path=None, file_path=None, parent_folder_path=None, extension=None):
    while(True):
        if not select:
            print('1. folder')
            print('2. parent folder')
            select = str(strip_quotes(input("Enter select process : ")))
            if not select:
                select = '1'
        if select == '1':
            if not folder_path:
                folder_path = strip_quotes(input('Enter folder path: '))
            if not extension:
                extension = strip_quotes(input('Enter target extension : '))
            print(folder_path)
            sub = get_specific_sub_folder_path(folder_path, 'face_speak')
            move_files_up(sub)

            select = None
            folder_path = None
                
        elif select == '2':
            if not parent_folder_path:
                parent_folder_path = strip_quotes(input('Enter parent folder path: '))
            folders = sub_path(parent_folder_path)
            print(folders)
            if folders:
                for i, folder in enumerate(folders):
                    sub = get_specific_sub_folder_path(folder, 'face_speak')
                    move_files_up(sub)
            select = None
            parent_folder_path = None
        else:
            select = None
            continue

if __name__ == "__main__":
    run()