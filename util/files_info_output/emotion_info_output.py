# -*- coding: utf-8 -*-
import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.library.junLib import *
from _workplace.library.junLib_video import get_files_info_mp4

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

def run(select='', emotion_type_folder_path=None, file_path=None, emotion_root_folder_path=None, extension=None):
    while(True):
        if not emotion_root_folder_path:
            emotion_root_folder_path = strip_quotes(input('Enter emotion folder path: '))
        emotion_folders = get_dir_sub_folder_path(emotion_root_folder_path)
        jpg_total_count = 0
        jpg_total_size = 0
        xml_total_count = 0
        xml_total_size = 0
        mp4_total_count = 0
        mp4_total_size = 0
        mp4_total_duration = 0

        if emotion_folders:
            for i, emotion_type_folder_path in enumerate(emotion_folders, 1):
                clear()
                print(f"{i}/{len(emotion_folders)}")
                speakers_folder_path = get_dir_sub_folder_path(emotion_type_folder_path)
                for j, speaker_folder_path in enumerate(speakers_folder_path, 1):
                    clear()
                    print(f"{i}/{len(emotion_folders)}\t{j}/{len(speakers_folder_path)}")
                    jpg_count, jpg_size, xml_count, xml_size, mp4_count, mp4_size, mp4_duration = process(speaker_folder_path)
                    jpg_total_count += jpg_count
                    jpg_total_size += jpg_size
                    xml_total_count += xml_count
                    xml_total_size += xml_size
                    mp4_total_count += mp4_count
                    mp4_total_size += mp4_size
                    mp4_total_duration += mp4_duration
                    print("jpg_count ", jpg_count, "\njpg_size ", jpg_size, "\nxml_count ", xml_count, "\nxml_size ", xml_size, "\nmp4_count ", mp4_count, "\nmp4_size ", mp4_size, "\nmp4_duration ", mp4_duration)
            result_file_path = join_folder_path(os.path.dirname(emotion_root_folder_path), 'emotion_result.txt')
            print("result : ", result_file_path)
            with open(result_file_path, 'w', encoding='utf-8') as file:
                file.write(f"jpg_total_count : {jpg_total_count} 개\n")
                file.write(f"jpg_total_size\n{jpg_total_size} byte\n{float(get_size_in_kb(jpg_total_size)):3f} kb\n{float(get_size_in_mb(jpg_total_size)):3f} mb\n\n")
                file.write(f"xml_total_count : {xml_total_count} 개\n")
                file.write(f"xml_total_size\n{xml_total_size} byte\n{float(get_size_in_kb(xml_total_size)):3f} kb\n{float(get_size_in_mb(xml_total_size)):3f} mb\n\n")
                file.write(f"mp4_total_count : {mp4_total_count}\n")
                file.write(f"mp4_total_size\n{mp4_total_size} byte\n{float(get_size_in_kb(mp4_total_size)):3f} kb\n{float(get_size_in_mb(mp4_total_size)):3f} mb\n\n")
                file.write(f"mp4_total_duration : {float(mp4_total_duration):3f} 초\n{seconds_to_hms(mp4_total_duration)} (시:분:초)\n{seconds_to_ms(mp4_total_duration)} (분:초)\n")
        emotion_root_folder_path = None

if __name__ == "__main__":
    run()