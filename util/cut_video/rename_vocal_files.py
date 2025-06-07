# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *

def process(file_path):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    parent = parent_path(file_path)
    refined_name = str(base_name).split('-')[0]
    new_path = join_folder_path(parent, refined_name)
    rename_and_move_file(file_path, new_path)

def run():
    print('1. folder\n2. file')
    select = str(strip_quotes(input("Enter select process : ")))
    if select == '1':
        folder_path = strip_quotes(input('Enter folder path: '))
        files = get_files_path_in_folder_via_ext(folder_path, 'mp3')
        for i, file in enumerate(files):
            process(file)

    elif select == '2':
        file_path = strip_quotes(input('Enter file path: '))


if __name__ == "__main__":
    run()