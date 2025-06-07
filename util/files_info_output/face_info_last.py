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
    jpg_count, jpg_size = get_files_info(speaker_folder_path, 'jpg')
    xml_count, xml_size = get_files_info(speaker_folder_path, 'xml')
    mp4_count, mp4_size, mp4_duration = get_files_info_mp4(speaker_folder_path)
    return jpg_count, jpg_size, xml_count, xml_size, mp4_count, mp4_size, mp4_duration
    # mp4_files = get_files_path_in_folder_via_ext(speaker_folder_path, 'mp4')
    # for i, mp4_file in enumerate(mp4_files):
    #     default_file_name, time_info, emt_speaker_info = os.path.splitext(os.path.basename(mp4_file))[0].split('-')
    #     jpg_files = get_files_path_in_folder_via_startwith(speaker_folder_path, f"{default_file_name}-{time_info}", 'jpg')
        
    #     process_file(mp4_file)

def run(select='', emotion_type_folder_path=None, file_path=None, face_root_folder_path=None, extension=None):
    while(True):
        if not face_root_folder_path:
            face_root_folder_path = strip_quotes(input('Enter emotion folder path: '))
        jpg_total_count = 0
        jpg_total_size = 0
        xml_total_count = 0
        xml_total_size = 0

        jpg_files = get_files_path_in_folder_via_ext(face_root_folder_path, 'jpg', True)
        jpg_total_count = len(jpg_files)
        for i, file in enumerate(jpg_files):
            jpg_size = os.path.getsize(file)
            jpg_total_size += jpg_size

        xml_files = get_files_path_in_folder_via_ext(face_root_folder_path, 'xml', True)
        xml_total_count = len(xml_files)
        for i, file in enumerate(xml_files):
            xml_size = os.path.getsize(file)
            xml_total_size += xml_size
        result_file_path = join_folder_path(os.path.dirname(face_root_folder_path), 'face_result.txt')
        print("result : ", result_file_path)
        with open(result_file_path, 'w', encoding='utf-8') as file:
            file.write(f"jpg_total_count : {jpg_total_count} 개\n")
            file.write(f"jpg_total_size\n{jpg_total_size:3f} byte\n{float(get_size_in_kb(jpg_total_size)):3f} kb\n{float(get_size_in_mb(jpg_total_size)):3f} mb\n\n")
            file.write(f"xml_total_count : {xml_total_count} 개\n")
            file.write(f"xml_total_size\n{xml_total_size:3f} byte\n{float(get_size_in_kb(xml_total_size)):3f} kb\n{float(get_size_in_mb(xml_total_size)):3f} mb\n\n")
        face_root_folder_path = None

if __name__ == "__main__":
    run()