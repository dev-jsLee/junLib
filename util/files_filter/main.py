# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from _workplace.library.junLib import *

def process(file_path):
    mp3_file = change_extension(file_path, 'mp3')
    if path_exist(mp3_file):
        delete_file(mp3_file)
    else:
        pass

def run(select='', folder_path=None, file_path=None, parent_folder_path=None, extension=None):
    NG_file = strip_quotes(input('Enter NGfile.txt: '))
    parent_folder_path = parent_path(NG_file)
    file_list = read_lines(NG_file)
    for i, file in enumerate(file_list):
        file_path = join_folder_path(parent_folder_path, file)
        process(file_path)

if __name__ == "__main__":
    run()