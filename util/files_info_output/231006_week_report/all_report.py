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

def process_emotion(emotion_root_folder_path):
    result = {
        'jpg' : {
            'count': 0,
            'size': 0
        },
        'xml' : {
            'count': 0,
            'size': 0
        },
        'mp4' : {
            'count': 0,
            'size': 0,
            'length' : 0
        },
    }
    emotion_folders = get_dir_sub_folder_path(emotion_root_folder_path)
    for i, emotion_folder_path in enumerate(emotion_folders, 1):
        speakers = get_dir_sub_folder_path(emotion_folder_path)
        for j, speaker_folder_path in enumerate(speakers, 1):
            print(f"emotion\n: process: {j}/{len(speakers)}, {i}/{len(emotion_folders)}")
            files = get_files_path_in_folder_at_all(speaker_folder_path)
            jpg_count, jpg_size = get_files_info(speaker_folder_path, 'jpg')
            print('jpg_count : ', jpg_count, '\njpg_size : ', jpg_size)
            result['jpg']['count'] += jpg_count
            result['jpg']['size'] += get_size_in_mb(jpg_size)

            xml_count, xml_size = get_files_info(speaker_folder_path, 'xml')
            print('xml_count : ', xml_count, '\nxml_size : ', xml_size)
            result['xml']['count'] += xml_count
            result['xml']['size'] += get_size_in_mb(xml_size)

            mp4_count, mp4_size, mp4_length = get_files_info_mp4(speaker_folder_path)
            print('mp4_count : ', xml_count, '\nmp4_size : ', xml_size, '\nmp4_length : ', mp4_length)
            result['mp4']['count'] += mp4_count
            result['mp4']['size'] += get_size_in_mb(mp4_size)
            result['mp4']['length'] += mp4_length
    return result

def process_speech(speech_root_folder_path):
    result = {
        'xml' : {
            'count': 0,
            'size': 0
        },
        'mp4' : {
            'count': 0,
            'size': 0,
            'length' : 0
        },
    }
    speaker_folders = get_dir_sub_folder_path(speech_root_folder_path)

    for i, speaker_folder_path in enumerate(speaker_folders, 1):
        print(f"speaker\n: process: {i}/{len(speaker_folders)}")
        xml_count, xml_size = get_files_info(speaker_folder_path, 'xml')
        print('xml_count : ', xml_count, '\nxml_size : ', xml_size)
        result['xml']['count'] += xml_count
        result['xml']['size'] += get_size_in_mb(xml_size)

        mp4_count, mp4_size, mp4_length = get_files_info_mp4(speaker_folder_path)
        print('mp4_count : ', xml_count, '\nmp4_size : ', xml_size, '\nmp4_length : ', mp4_length)
        result['mp4']['count'] += mp4_count
        result['mp4']['size'] += get_size_in_mb(mp4_size)
        result['mp4']['length'] += mp4_length
    return result

def process_face(face_root_folder_path):
    result = {
        'jpg' : {
            'count': 0,
            'size': 0
        },
        'xml' : {
            'count': 0,
            'size': 0
        },
    }
    targt_folder_path = face_root_folder_path
    folders = get_dir_sub_folder_path(face_root_folder_path)
    for i, folder_path in enumerate(folders):
        folder_name = os.path.basename(folder_path)
        if str(folder_name).strip() == 'face':
            targt_folder_path = folder_path
        else:
            continue
    print(f"face\ttarget: {os.path.basename(os.path.dirname(face_root_folder_path))}")
    jpg_count, jpg_size = get_files_info(targt_folder_path, 'jpg')
    print('jpg_count : ', jpg_count, '\njpg_size : ', jpg_size)
    result['jpg']['count'] += jpg_count
    result['jpg']['size'] += get_size_in_mb(jpg_size)
            
    xml_count, xml_size = get_files_info(targt_folder_path, 'xml')
    print('xml_count : ', xml_count, '\nxml_size : ', xml_size)
    result['xml']['count'] += xml_count
    result['xml']['size'] += get_size_in_mb(xml_size)
    return result

def process_speaker(speaker_root_folder_path):
    result = {
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
    print(f"face\ttarget: {os.path.basename(os.path.dirname(speaker_root_folder_path))}")
    xml_count, xml_size = get_files_info(speaker_root_folder_path, 'xml')
    print('xml_count : ', xml_count, '\nxml_size : ', xml_size)
    result['xml']['count'] += xml_count
    result['xml']['size'] += get_size_in_mb(xml_size)

    mp3_count, mp3_size = get_files_info(speaker_root_folder_path, 'mp3')
    print('mp3_count : ', mp3_count, '\nmp3_size : ', mp3_size)
    result['mp3']['count'] += mp3_count
    result['mp3']['size'] += get_size_in_mb(mp3_size)
    speakers = get_dir_sub_folder_path(speaker_root_folder_path)

    for j, speaker_folder_path in enumerate(speakers):
        mp4_count, mp4_size, mp4_length = get_files_info_mp4(speaker_folder_path)
        print('mp4_count : ', xml_count, '\nmp4_size : ', xml_size, '\nmp4_length : ', mp4_length)
        result['mp4']['count'] += mp4_count
        result['mp4']['size'] += get_size_in_mb(mp4_size)
        result['mp4']['length'] += mp4_length
    return result

def run():
    folder_path = strip_quotes(input("Enter folder path : "))
    remove_empty_folders(folder_path)
    yyyymm_folders = get_dir_sub_folder_path(folder_path)
    emotion = {
        'jpg' : {
            'count': 0,
            'size': 0
        },
        'xml' : {
            'count': 0,
            'size': 0
        },
        'mp4' : {
            'count': 0,
            'size': 0,
            'length' : 0
        },
    }
    
    speech = {
        'xml' : {
            'count': 0,
            'size': 0
        },
        'mp4' : {
            'count': 0,
            'size': 0,
            'length' : 0
        },
    }
    
    face = {
        'jpg' : {
            'count': 0,
            'size': 0
        },
        'xml' : {
            'count': 0,
            'size': 0
        },
    }
    
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
    
    for i, yymmdd_folder_path in enumerate(yyyymm_folders, 1):
        print(f"{i}/{len(yyyymm_folders)}")
        process_folders = get_dir_sub_folder_path(yymmdd_folder_path)
        for j, process_folder_path in enumerate(process_folders, 1):
            process_name = os.path.basename(process_folder_path)
            process_name = str(process_name).strip()
            print(f"process : {process_name}")
            if process_name == "감정인식":
                emotion_info = process_emotion(process_folder_path)
                for ext, info in emotion_info.items():
                    for att, value in emotion_info[ext].items():
                        emotion[ext][att] += emotion_info[ext][att]

            elif process_name == "구화인식":
                speech_info = process_speech(process_folder_path)
                for ext, info in speech_info.items():
                    for att, value in speech_info[ext].items():
                        speech[ext][att] += speech_info[ext][att]

            elif process_name == "얼굴인식":
                face_info = process_face(process_folder_path)
                for ext, info in face_info.items():
                    for att, value in face_info[ext].items():
                        face[ext][att] += face_info[ext][att]

            elif process_name == "화자인식":
                speaker_info = process_speaker(process_folder_path)
                for ext, info in speaker_info.items():
                    for att, value in speaker_info[ext].items():
                        speaker[ext][att] += speaker_info[ext][att]

    emotion_txt_file_path = join_folder_path(os.path.dirname(folder_path), f'{os.path.basename(folder_path)}_emotion.txt')
    emotion_text = ''
    emotion_text += f"jpg_count : {emotion['jpg']['count']} 개\n"
    emotion_text += f"jpg_size : {emotion['jpg']['size']} mb\n"
    emotion_text += f"xml_count : {emotion['xml']['count']} 개\n"
    emotion_text += f"xml_size : {emotion['xml']['size']} mb\n"
    emotion_text += f"mp4_count : {emotion['mp4']['count']} 개\n"
    emotion_text += f"mp4_size : {emotion['mp4']['size']} mb\n"
    hms_str = seconds_to_hms(emotion['mp4']['length'])
    emotion_text += f"mp4_length : {emotion['mp4']['length']} 초\t{hms_str}\n"
    write_to_file(emotion_txt_file_path, emotion_text)
    print(f"{emotion_txt_file_path} done.")

    speech_txt_file_path = join_folder_path(os.path.dirname(folder_path), f'{os.path.basename(folder_path)}_speech.txt')
    speech_text = ''
    speech_text += f"xml_count : {speech['xml']['count']} 개\n"
    speech_text += f"xml_size : {speech['xml']['size']} mb\n"
    speech_text += f"mp4_count : {speech['mp4']['count']} 개\n"
    speech_text += f"mp4_size : {speech['mp4']['size']} mb\n"
    hms_str = seconds_to_hms(speech['mp4']['length'])
    speech_text += f"mp4_length : {speech['mp4']['length']} 초\t{hms_str}\n"
    write_to_file(speech_txt_file_path, speech_text)
    print(f"{speech_txt_file_path} done.")

    face_txt_file_path = join_folder_path(os.path.dirname(folder_path), f'{os.path.basename(folder_path)}_face.txt')
    face_text = ''
    face_text += f"jpg_count : {face['jpg']['count']} 개\n"
    face_text += f"jpg_size : {face['jpg']['size']} mb\n"
    face_text += f"xml_count : {face['xml']['count']} 개\n"
    face_text += f"xml_size : {face['xml']['size']} mb\n"
    write_to_file(face_txt_file_path, face_text)
    print(f"{face_txt_file_path} done.")

    speaker_txt_file_path = join_folder_path(os.path.dirname(folder_path), f'{os.path.basename(folder_path)}_speaker.txt')
    speaker_text = ''
    speaker_text += f"xml_count : {speaker['xml']['count']} 개\n"
    speaker_text += f"xml_size : {speaker['xml']['size']} mb\n"
    speaker_text += f"mp3_count : {speaker['mp3']['count']} 개\n"
    speaker_text += f"mp3_size : {speaker['mp3']['size']} mb\n"
    speaker_text += f"mp4_count : {speaker['mp4']['count']} 개\n"
    speaker_text += f"mp4_size : {speaker['mp4']['size']} mb\n"
    hms_str = seconds_to_hms(speaker['mp4']['length'])
    speaker_text += f"mp4_length : {speaker['mp4']['length']} 초\t{hms_str}\n"
    write_to_file(speaker_txt_file_path, speaker_text)
    print(f"{speaker_txt_file_path} done.")

if __name__ == "__main__":
    run()