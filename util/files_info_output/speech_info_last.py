# -*- coding: utf-8 -*-
import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.library.junLib import *
from _workplace.library.junLib_video import get_files_info_mp4

def process(speaker_folder_path):
    # jpg_files = get_files_path_in_folder_via_ext(speaker_folder_path, 'jpg')
    mp4_count, mp4_size, mp4_duration = get_files_info_mp4(speaker_folder_path)

    return mp4_count, mp4_size, mp4_duration
    # mp4_files = get_files_path_in_folder_via_ext(speaker_folder_path, 'mp4')
    # for i, mp4_file in enumerate(mp4_files):
    #     default_file_name, time_info, emt_speaker_info = os.path.splitext(os.path.basename(mp4_file))[0].split('-')
    #     jpg_files = get_files_path_in_folder_via_startwith(speaker_folder_path, f"{default_file_name}-{time_info}", 'jpg')
        
    #     process_file(mp4_file)

def run(select='', speaker_folder_path=None, emotion_root_folder_path=None, speech_root_folder_path=None, extension=None):
        # select = strip_quotes(input("Enter select : "))
        # if select == '1':
            speech_root_folder_path = speech_root_folder_path or strip_quotes(input('Enter speech root folder path: '))
            xml_total_count = 0
            xml_total_size = 0
            mp4_total_count = 0
            mp4_total_size = 0
            mp4_total_duration = 0
            speaker_folders = get_dir_sub_folder_path(speech_root_folder_path)
            if speaker_folders:
                for i, speaker_folder_path in enumerate(speaker_folders, 1):
                    clear()
                    print(f"{i}/{len(speaker_folders)}")
                    xml_count, xml_size = get_files_info(speaker_folder_path, 'xml')
                    xml_total_count += xml_count
                    xml_total_size += xml_size

                    mp4_count, mp4_size, mp4_duration = get_files_info_mp4(speaker_folder_path)
                    mp4_total_count += mp4_count
                    mp4_total_size += mp4_size
                    mp4_total_duration += mp4_duration
                    print("xml_count ", xml_count, ", xml_size ", xml_size)
                    print("mp4_count ", mp4_count, ", mp4_size ", mp4_size, ", mp4_duration ", mp4_duration)
                print(os.path.dirname(speech_root_folder_path))
                result_file_path = join_folder_path(os.path.dirname(speech_root_folder_path), 'speech_result.txt')
                print(result_file_path)
                with open(result_file_path, 'w', encoding='utf-8') as file:
                    file.write(f"xml_total_count : {xml_total_count} 개\n")
                    file.write(f"xml_total_size\n{xml_total_size} byte\n{float(get_size_in_kb(xml_total_size)):3f} kb\n{float(get_size_in_mb(xml_total_size)):3f} mb\n\n")
                    file.write(f"mp4_total_count : {mp4_total_count}\n")
                    file.write(f"mp4_total_size\n{mp4_total_size} byte\n{float(get_size_in_kb(mp4_total_size)):3f} kb\n{float(get_size_in_mb(mp4_total_size)):3f} mb\n\n")
                    file.write(f"mp4_total_duration : {mp4_total_duration:3f} 초\n{seconds_to_ms(mp4_total_duration)} (분:초)\n{seconds_to_hms(mp4_total_duration)} (시:분:초)\n")
            speech_root_folder_path = None
        # elif select == '2':
        #     emotion_root_folder_path = emotion_root_folder_path or strip_quotes(input('Enter emotion_root_folder path: '))
        #     xml_total_count = 0
        #     xml_total_size = 0
        #     mp4_total_count = 0
        #     mp4_total_size = 0
        #     mp4_total_duration = 0
        #     yymmdd_folders = get_dir_sub_folder_path(emotion_root_folder_path)
        #     for i, yymmdd in enumerate(yymmdd_folders):
        #         print(os.path.basename(yymmdd))
        #         speech_folder = join_folder_path(yymmdd, 'speaker')
        #         speaker_folders = get_dir_sub_folder_path(speech_folder)
        #         if speaker_folders:
        #             for i, speaker_folder_path in enumerate(speaker_folders, 1):
        #                 print(f"{i}/{len(speaker_folders)}")
        #                 xml_count, xml_size = get_files_info(speaker_folder_path, 'xml')
        #                 xml_total_count += xml_count
        #                 xml_total_size += xml_size

        #                 mp4_count, mp4_size, mp4_duration = get_files_info_mp4(speaker_folder_path)
        #                 mp4_total_count += mp4_count
        #                 mp4_total_size += mp4_size
        #                 mp4_total_duration += mp4_duration
        #                 # print("xml_count ", xml_count, ", xml_size ", xml_size)
        #                 # print("mp4_count ", mp4_count, ", mp4_size ", mp4_size, ", mp4_duration ", mp4_duration)
        #     result_file_path = join_folder_path(os.path.dirname(emotion_root_folder_path), 'speaker_result.txt')
        #     print(result_file_path)
        #     with open(result_file_path, 'w', encoding='utf-8') as file:
        #         file.write(f"xml_total_count : {xml_total_count} 개\n")
        #         file.write(f"xml_total_size\n{xml_total_size} byte\n{float(get_size_in_kb(xml_total_size)):3f} kb\n{float(get_size_in_mb(xml_total_size)):3f} mb\n\n")
        #         file.write(f"mp4_total_count : {mp4_total_count}\n")
        #         file.write(f"mp4_total_size\n{mp4_total_size} byte\n{float(get_size_in_kb(mp4_total_size)):3f} kb\n{float(get_size_in_mb(mp4_total_size)):3f} mb\n\n")
        #         file.write(f"mp4_total_duration : {mp4_total_duration:3f} 초\n{seconds_to_ms(mp4_total_duration)} (분:초)\n{seconds_to_hms(mp4_total_duration)} (시:분:초)\n")
        #     emotion_root_folder_path = None
        #     input("done.")

def check():
    speaker_root_folder_path = strip_quotes(input("enter folder path : "))
    print(os.path.dirname(speaker_root_folder_path))
    result_file_path = join_folder_path(os.path.dirname(speaker_root_folder_path), 'speaker_result.txt')
    print(result_file_path)
if __name__ == "__main__":
    # check()
    run()