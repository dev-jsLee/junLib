# -*- coding: utf-8 -*-
import os
import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *

def run(select='', folder_path=None, parent_folder_path=None):
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
            remove_empty_folders(folder_path)
            select = None
            folder_path = None
                
        elif select == '2':
            if not parent_folder_path:
                parent_folder_path = strip_quotes(input('Enter parent folder path: '))
            folders = sub_path(parent_folder_path)
            if folders:
                for i, folder in enumerate(folders):
                    remove_empty_folders(folder)
            select = None
            parent_folder_path = None
        else:
            select = None
            continue

if __name__ == "__main__":
    run()