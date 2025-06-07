import os
import sys
from __init__ import source_code_path
sys.path.append(source_code_path)
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *

def process(folder_path=None, target_folder_name=None):
    folder_path = folder_path or strip_quotes(input("Enter folder path : "))
    yymmdd_folders = get_dir_sub_folder_path(folder_path)
    target_folder_name = target_folder_name or strip_quotes(input("Enter folder name : "))
    for i, yymmdd in enumerate(yymmdd_folders):
        delete_folders_by_name(yymmdd, target_folder_name)

def run(select=None, target_folder_name=None, dir_folder_path=None, folder_path=None, parent_folder_path=None):
    if not select:
        print('1. direct folder\n2. sub folder\n3. sub sub folder')
    select = select or strip_quotes(input('Select Process : ')) or '1'
    target_folder_name = target_folder_name or strip_quotes(input("Enter target folder name : ")) or 'backup'
    if select == '1':
        dir_folder_path = dir_folder_path or strip_quotes(input("Enter dir folder path : "))
        delete_folders_by_name(dir_folder_path, target_folder_name)
    elif select == '2':
        folder_path = folder_path or strip_quotes(input("Enter folder path : "))
        process(target_folder_name=target_folder_name, folder_path=folder_path)
    elif select == '3':
        parent_folder_path = parent_folder_path or strip_quotes(input("Enter parent folder path : "))
        folders = get_dir_sub_folder_path(parent_folder_path)
        for i, folder in enumerate(folders):
            process(folder, target_folder_name)

if __name__ == "__main__":
    run()