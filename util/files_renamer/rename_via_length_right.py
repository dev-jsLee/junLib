# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *

def process(file_path, length, new_word):
    parent = parent_path(file_path)
    file_name, ext = split_filename(basename(file_path))
    # ext = '.ext'
    new_name = file_name.replace(file_name[-int(length):], new_word)
    new_path = join_folder_path(parent, new_name + ext)
    copy_and_rename_file(file_path, new_path)
    move_file(file_path, join_folder_path(parent, 'delete', basename(file_path)))

def run():
    folder_path = strip_quotes(input('Enter folder path : '))
    length = strip_quotes(input('Enter remove name length from right : '))
    replace_word = strip_quotes(input('Enter new word instead of removed word : '))
    ext = strip_quotes(input("Enter extension(default all): "))
    files = None
    if ext:
        files = get_files_path_in_folder_via_ext(folder_path, ext)
    else:
        files = get_files_path_in_folder_at_all(folder_path)
    for i, file in enumerate(files):
        process(file, length, replace_word)
        pass
    pass

if __name__ == "__main__":
    run()