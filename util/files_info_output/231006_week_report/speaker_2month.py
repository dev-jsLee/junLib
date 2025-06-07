# -*- coding: utf-8 -*-
import os
import sys
current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)
_workplace_folder_path = current_directory

while(True):
    if os.path.basename(_workplace_folder_path) == '_workplace':
        break
    else:
        _workplace_folder_path = os.path.dirname(_workplace_folder_path)
        continue
source_code_path = os.path.dirname(_workplace_folder_path)
_gitlab_path = os.path.dirname(source_code_path)
root_folder_path = os.path.dirname(_gitlab_path)
sys.path.append(source_code_path)
from _workplace.library.junLib import *
def process_finalworking(speaker_root_folder_path):
    speakers = get_dir_sub_folder_path(speaker_root_folder_path)
    speaker = {
        'mp4' : {
            'count': 0,
            'size': 0,
            'length' : 0
        },
    }
    for i, speaker_folder_path in enumerate(speakers, 1):
        print(f"speaker\t{i}/{len(speakers)}")
        mp4_count, mp4_size, mp4_length = get_files_info_mp4(speaker_folder_path, True)
        
        speaker['mp4']['count'] += mp4_count
        speaker['mp4']['size'] += mp4_size
        speaker['mp4']['length'] += mp4_length
    return speaker

def process(yymmdd_folder_path):
    speaker_root_folder_path = join_folder_path(yymmdd_folder_path, 'speaker')
    speakers = get_dir_sub_folder_path(speaker_root_folder_path)
    speaker = {
        'mp4' : {
            'count': 0,
            'size': 0,
            'length' : 0
        },
    }
    for i, speaker_folder_path in enumerate(speakers, 1):
        print(f"speaker\t{i}/{len(speakers)}")
        mp4_count, mp4_size, mp4_length = get_files_info_mp4(speaker_folder_path, True)
        
        speaker['mp4']['count'] += mp4_count
        speaker['mp4']['size'] += mp4_size
        speaker['mp4']['length'] += mp4_length
    return speaker

def run(select='', yymmdd_folder_path=None, emotion_folder_path=None):
        speaker = {
            'xml' : {
                'count': 0,
                'size': 0
            },
            'mp4' : {
                'count': 0,
                'size': 0,
                'length' : 0
            },
            'mp3' : {
                'count': 0,
                'size': 0,
                'length' : 0
            }
        }
        select = select or '1'

        if select == '1' or select == 'emotion':
            emotion_folder_path = emotion_folder_path or strip_quotes(input('Enter emotion folder path: '))
            yymmdd_folders = get_dir_sub_folder_path(emotion_folder_path)
            if yymmdd_folders:
                for i, yymmdd_folder_path in enumerate(yymmdd_folders, 1):
                    print(f"yymmdd\t{i}/{len(yymmdd_folders)}")
                    speaker_info = process(yymmdd_folder_path)
                    for ext, info in speaker_info.items():
                        for att, value in speaker_info[ext].items():
                            speaker[ext][att] += speaker_info[ext][att]
            speaker_txt_file_path = join_folder_path(os.path.dirname(emotion_folder_path), f'{os.path.basename(emotion_folder_path)}_speaker.txt')
            speaker_text = ''
            speaker_text += f"mp4_count : {speaker['mp4']['count']} 개\n"
            speaker_text += f"mp4_size : {get_size_in_mb(speaker['mp4']['size'])} mb\n"
            hms_str = seconds_to_hms(speaker['mp4']['length'])
            speaker_text += f"mp4_length : {speaker['mp4']['length']} 초\t{hms_str}\n"
            write_to_file(speaker_txt_file_path, speaker_text)
            print(f"{speaker_txt_file_path} done.")
            select = None
            emotion_folder_path = None

        elif select == '2':
            speaker_root_folder_path = strip_quotes(input("Enter speaker root folder path in final_working : "))
            speaker_info = process_finalworking(speaker_root_folder_path)
            for ext, info in speaker_info.items():
                for att, value in speaker_info[ext].items():
                        speaker[ext][att] += speaker_info[ext][att]
            speaker_txt_file_path = join_folder_path(os.path.dirname(speaker_root_folder_path), f'{os.path.basename(speaker_root_folder_path)}_speaker.txt')
            speaker_text = ''
            speaker_text += f"mp4_count : {speaker['mp4']['count']} 개\n"
            speaker_text += f"mp4_size : {get_size_in_mb(speaker['mp4']['size'])} mb\n"
            hms_str = seconds_to_hms(speaker['mp4']['length'])
            speaker_text += f"mp4_length : {speaker['mp4']['length']} 초\t{hms_str}\n"
            write_to_file(speaker_txt_file_path, speaker_text)
            print(f"{speaker_txt_file_path} done.")
            select = None
            emotion_folder_path = None

        # elif select == '2' or select == 'yymmdd':
        #     yymmdd_folder_path = yymmdd_folder_path or strip_quotes(input('Enter emotion/yymmdd folder path: '))
        #     process(yymmdd_folder_path)
        #     select = None
        #     yymmdd_folder_path = None

if __name__ == "__main__":
    run(select='2')