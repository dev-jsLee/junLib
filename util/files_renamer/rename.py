# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *

def process(file_path, default_name):
    mp4_file_path = change_extension(file_path, 'mp4')
    xml_file_name = split_filename(basename(file_path))[0]
    specific_num = xml_file_name.split('_')[-1]
    parent = parent_path(file_path)
    # specific_num = xml_file_name.split('_')[-1]
    copy_and_rename_file(file_path, join_folder_path(parent, default_name + '_' + specific_num + '.xml'))
    copy_and_rename_file(mp4_file_path, join_folder_path(parent, default_name + '_' + specific_num + '.mp4'))


def run():
    folder_path = strip_quotes(input('Enter folder path : '))
    xml_files = get_files_path_in_folder_via_ext(folder_path, 'xml')
    csv_files = get_files_path_in_folder_via_ext(folder_path, 'csv')
    for i, xml_file_path in enumerate(xml_files):
        default_part = None
        for i, csv_file in enumerate(csv_files):
            default_name = split_filename(basename(csv_file))[0]
            default_part = default_name.split('_')[-2] + '_' + default_name.split('_')[-1]
            if str(xml_file_path).__contains__(default_part):
                process(xml_file_path, default_name)

if __name__ == "__main__":
    run()