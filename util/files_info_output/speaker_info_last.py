# -*- coding: utf-8 -*-
import os
import sys
current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)
_workplace_folder_path = current_directory

while(True):
    print('folder : ', _workplace_folder_path)
    if os.path.basename(_workplace_folder_path) == '_workplace':
        print('this : ', os.path.basename(_workplace_folder_path))
        break
    else:
        _workplace_folder_path = os.path.dirname(_workplace_folder_path)
        continue
source_code_path = os.path.dirname(_workplace_folder_path)
_gitlab_path = os.path.dirname(source_code_path)
root_folder_path = os.path.dirname(_gitlab_path)
sys.path.append(source_code_path)
from _workplace.library.junLib import *

def process(speaker_folder_path):
    # jpg_files = get_files_path_in_folder_via_ext(speaker_folder_path, 'jpg')
    mp4_count, mp4_size, mp4_duration = get_files_info_mp4(speaker_folder_path)

    return mp4_count, mp4_size, mp4_duration
    # mp4_files = get_files_path_in_folder_via_ext(speaker_folder_path, 'mp4')
    # for i, mp4_file in enumerate(mp4_files):
    #     default_file_name, time_info, emt_speaker_info = os.path.splitext(os.path.basename(mp4_file))[0].split('-')
    #     jpg_files = get_files_path_in_folder_via_startwith(speaker_folder_path, f"{default_file_name}-{time_info}", 'jpg')
        
    #     process_file(mp4_file)

def run(select='', speaker_folder_path=None, file_path=None, speaker_root_folder_path=None, extension=None):
    while(True):
        if not speaker_root_folder_path:
            speaker_root_folder_path = strip_quotes(input('Enter speaker root folder path: '))
        xml_total_count = 0
        xml_total_size = 0
        txt_total_count = 0
        txt_total_size = 0
        mp4_total_count = 0
        mp4_total_size = 0
        mp4_total_duration = 0
        xml_total_count, xml_total_size = get_files_info(speaker_root_folder_path, 'xml')
        txt_total_count, txt_total_size = get_files_info(speaker_root_folder_path, 'txt')
        mp3_total_count, mp3_total_size = get_files_info(speaker_root_folder_path, 'mp3')
        print("xml_total_count : ", xml_total_count, "\nxml_total_size : ", xml_total_size)
        speaker_folders = get_dir_sub_folder_path(speaker_root_folder_path)
        if speaker_folders:
            for i, speaker_folder_path in enumerate(speaker_folders, 1):
                print(f"{i}/{len(speaker_folders)}")
                mp4_count, mp4_size, mp4_duration = process(speaker_folder_path)
                mp4_total_count += mp4_count
                mp4_total_size += mp4_size
                mp4_total_duration += mp4_duration
                print("mp4_count ", mp4_count, ", mp4_size ", mp4_size, ", mp4_duration ", mp4_duration)
            print(os.path.dirname(speaker_root_folder_path))
            result_file_path = join_folder_path(os.path.dirname(speaker_root_folder_path), 'speaker_result.txt')
            print(result_file_path)
            with open(result_file_path, 'w', encoding='utf-8') as file:
                file.write(f"xml_total_count : {xml_total_count} 개\n")
                file.write(f"xml_total_size\n{xml_total_size} byte\n{get_size_in_kb(xml_total_size):3f} kb\n{get_size_in_mb(xml_total_size):3f} mb\n\n")
                file.write(f"txt_total_count : {txt_total_count} 개\n")
                file.write(f"txt_total_size\n{txt_total_size} byte\n{get_size_in_kb(txt_total_size):3f} kb\n{get_size_in_mb(txt_total_size):3f} mb\n\n")
                file.write(f"mp3_total_count : {mp3_total_count} 개\n")
                file.write(f"mp3_total_size\n{mp3_total_size} byte\n{get_size_in_kb(mp3_total_size):3f} kb\n{get_size_in_mb(mp3_total_size):3f} mb\n\n")
                file.write(f"mp4_total_count : {mp4_total_count}\n")
                file.write(f"mp4_total_size\n{mp4_total_size} byte\n{get_size_in_kb(mp4_total_size):3f} kb\n{get_size_in_mb(mp4_total_size):3f} mb\n\n")
                file.write(f"mp4_total_duration : {mp4_total_duration} 초\n{seconds_to_ms(mp4_total_duration)} (분:초)\n{seconds_to_hms(mp4_total_duration)} (시:분:초)\n")
        speaker_root_folder_path = None

def check():
    speaker_root_folder_path = strip_quotes(input("enter folder path : "))
    print(os.path.dirname(speaker_root_folder_path))
    result_file_path = join_folder_path(os.path.dirname(speaker_root_folder_path), 'speaker_result.txt')
    print(result_file_path)
if __name__ == "__main__":
    # check()
    run()