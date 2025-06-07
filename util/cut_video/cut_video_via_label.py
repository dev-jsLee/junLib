# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *
from _workplace.util.cut_video.cut_video import cut_time_by_time as cuttime
from _workplace.util.media_files_control import transfer_mp4_to_mp3 as trans

def process(mp4_file_path, label_file_path):
    folder_path = parent_path(mp4_file_path)
    default_output_folder_path = create_folder(join_folder_path(folder_path, os.path.splitext(os.path.basename(mp4_file_path))[0]))
    obj = cuttime(mp4_file_path)
    lines = read_lines(label_file_path)
    for i, line in enumerate(lines):
        starttime, endtime, text = line.split('\t')
        text = text.strip().replace('?', '__').replace('.', '')
        output_file_name = '{}_{}_{}.mp4'.format(starttime, endtime, text.replace('\n', '').replace('\n', ''))
        output_file_path = join_folder_path(default_output_folder_path, output_file_name)
        obj.cut_video_time_no_stamp(starttime, endtime, output_file_path)
    trans.run('2', output_file_path)
        

def run():
    print('1. folder\n2. file')
    select = str(strip_quotes(input("Enter select process : ")))
    if select == '1':
        folder_path = strip_quotes(input('Enter folder path: '))
        mp4_files = get_files_path_in_folder_via_ext(folder_path, 'mp4')
        for i, mp4_file in enumerate(mp4_files):
            label_file_path = change_extension(mp4_file, 'txt')
            process(mp4_file, label_file_path)
            
    elif select == '2':
        mp4_file_path = strip_quotes(input('Enter mp4 file path: '))
        label_file_path = strip_quotes(input('Enter txt(label) file path: '))
        process(mp4_file_path, label_file_path)

if __name__ == "__main__":
    run()