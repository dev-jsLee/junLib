# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *

def process(file_path, target_word, new_word):
    parent = parent_path(file_path)
    file_name, ext = split_filename(basename(file_path))
    # ext = '.ext'
    if file_name.__contains__(target_word):
        new_name = file_name.replace(target_word, new_word)
        file_basename, time_info, speaker = new_name.split('-')
        start, end = time_info.split('_')
        new_name = new_name.replace(time_info, f"{float(start):.3f}_{float(end):.3f}")
        print(new_name)
        new_path = join_folder_path(parent, new_name + ext)
        if not path_exist(new_path):
            copy_and_rename_file(file_path, new_path)
        move_file(file_path, join_folder_path(parent, 'delete', basename(file_path)))

def run(folder_path=None, target_word=None, replace_word=None):
    folder_path = folder_path or strip_quotes(input('Enter folder path : '))
    target_word = target_word or strip_quotes(input('Enter remove target_word : '))
    if replace_word == '':
        files = get_files_path_at_all(folder_path)
        for i, file in enumerate(files):
            process(file, target_word, '')
        return
    replace_word = replace_word or strip_quotes(input('Enter new word instead of removed word : '))
    files = get_files_path_at_all(folder_path)
    for i, file in enumerate(files):
        process(file, target_word, replace_word)

def parent_run(parent_folder_path=None, target_word=None, replace_word=None):
    parent_folder_path = parent_folder_path or strip_quotes(input("Enter parent folder path : "))
    delete_folders_by_name(parent_folder_path, 'delete')
    target_word = target_word or strip_quotes(input('Enter remove target_word : '))
    if replace_word == None:
        replace_word = strip_quotes(input('Enter new word instead of removed word : '))
    folders= get_dir_sub_folder_path(parent_folder_path)
    for i, folder in enumerate(folders):
        run(folder, target_word, replace_word)
if __name__ == "__main__":
    # run()
    # parent_run()
    folder_path = strip_quotes(input('Enter emotion folder : '))
    delete_folders_by_name(folder_path, 'delete')
    # speaker_folders = get_sub_folder_path(folder_path)
    # for i, speaker_folder in enumerate(speaker_folders):
    #     run(target_word='-neutral_', replace_word='-', folder_path=speaker_folder)