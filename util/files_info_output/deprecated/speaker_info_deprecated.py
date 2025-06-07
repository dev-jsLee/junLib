# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from _workplace.library.junLib import *
from _workplace.library.junLib_xml_class_json import *
import moviepy.editor as mp
def get_directory_ext_stats(directory, target_ext:str='xml'):
    total_files = 0
    total_size = 0  # in bytes

    # List files in the given directory
    for filename in os.listdir(directory):
        if filename.endswith(target_ext):
            total_files += 1
            filepath = os.path.join(directory, filename)
            
            # Get size of the file
            total_size += os.path.getsize(filepath)

    return total_files, total_size

def get_directory_mp4_stats(directory):
    total_files = 0
    total_duration = 0  # in seconds
    total_size = 0  # in bytes

    # List files in the given directory
    for filename in os.listdir(directory):
        if filename.endswith('.mp4'):
            total_files += 1
            filepath = os.path.join(directory, filename)
            
            # Get duration of the video
            clip = mp.VideoFileClip(filepath)
            total_duration += clip.duration
            
            # Get size of the file
            total_size += os.path.getsize(filepath)
            clip.close()

    return total_files, total_duration, total_size

def get_subfolder_mp4_stats(directory):
    total_files = 0
    total_duration = 0  # in seconds
    total_size = 0  # in bytes
    
    subs = get_dir_sub_folder_path(directory)

    for i, folder in enumerate(subs):
        print("folder ", folder)
        files = get_files_path_in_folder_via_ext(folder, 'mp4')
        for j, filepath in enumerate(files):
            print("filepath : ", filepath)
            total_files += 1
            
            # Get duration of the video
            clip = mp.VideoFileClip(filepath)
            total_duration += clip.duration
            
            # Get size of the file
            total_size += os.path.getsize(filepath)
            clip.close()
        # total_file, duration, size = get_directory_mp4_stats(folder)
        # total_files += total_file
        # total_duration += duration
        # total_size += size
    print("total_files ", total_files)
    print("total_duration ", total_duration)
    print("total_size", total_size)
    # # Walk through directory and subdirectories
    # for dirpath, dirnames, filenames in os.walk(directory):
    #     # Skip the root directory
    #     if dirpath == directory:
    #         continue

    #     for filename in filenames:
    #         print("get_subfolder_mp4_stats\t", "filename :\t", filename)
    #         if filename.endswith('.mp4'):
    #             total_files += 1
    #             filepath = os.path.join(dirpath, filename)
                
    #             # Get duration of the video
    #             clip = mp.VideoFileClip(filepath)
    #             total_duration += clip.duration
                
    #             # Get size of the file
    #             total_size += os.path.getsize(filepath)
    #             clip.close()

    return total_files, total_duration, total_size

def get_mp4_at_all_stats(directory):
    total_files = 0
    total_duration = 0  # in seconds
    total_size = 0  # in bytes

    # Walk through directory and subdirectories
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.mp4'):
                total_files += 1
                filepath = os.path.join(dirpath, filename)
                
                # Get duration of the video
                clip = mp.VideoFileClip(filepath)
                total_duration += clip.duration
                
                # Get size of the file
                total_size += os.path.getsize(filepath)
                clip.close()

    return total_files, total_duration, total_size

def get_mp3_at_all_stats(directory):
    total_files = 0
    total_duration = 0  # in seconds
    total_size = 0  # in bytes

    # Walk through directory and subdirectories
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.mp3'):
                total_files += 1
                filepath = os.path.join(dirpath, filename)
                
                # Get duration of the video
                clip = mp.VideoFileClip(filepath)
                total_duration += clip.duration
                
                # Get size of the file
                total_size += os.path.getsize(filepath)
                clip.close()

    return total_files, total_duration, total_size

def seconds_to_hms(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"



def process(directory):
    total_files, total_duration, total_size = get_mp4_at_all_stats(directory)
    sub_files, sub_duration, sub_size = get_subfolder_mp4_stats(directory)
    source_files, source_duration, source_size = get_directory_mp4_stats(directory)
    xml_files, xml_size = get_directory_ext_stats(directory, 'xml')
    txt_files, txt_size = get_directory_ext_stats(directory, 'txt')
    mp3_files, mp3_duration, mp3_size = get_mp3_at_all_stats(directory)
    # Convert total_duration to hours:minutes:seconds format
    hms_duration = seconds_to_hms(total_duration)
    sub_hms = seconds_to_hms(sub_duration)
    source_hms = seconds_to_hms(source_duration)

    # Convert total_size to MB
    size_in_mb = total_size / (1024 * 1024)
    sub_size_in_mb = sub_size / (1024 * 1024)
    source_size_in_mb = source_size / (1024 * 1024)
    xml_size_in_mb = xml_size / (1024 * 1024)

    json_data = {
        'xml_files':{
            '__text__': xml_files
        },
        'xml_size_in_mb': {
            '__text__': xml_size_in_mb
        },
        'total_files': {
            '__text__': total_files
        },
        'hms_duration': {
            '__text__': hms_duration
        },
        'total_duration': {
            '__text__': total_duration
        },
        'size_in_mb': {
            '__text__': size_in_mb
        },
        'source_files': {
            '__text__': source_files
        },
        'source_hms': {
            '__text__': source_hms
        },
        'source_size_in_mb': {
            '__text__': source_size_in_mb
        },
        'sub_files': {
            '__text__': sub_files
        },
        'sub_duration': {
            '__text__': sub_duration
        },
        'sub_size_in_mb': {
            '__text__': sub_size_in_mb
        }
    }


    texts = []
    texts.append(f"{xml_files}\n")
    texts.append(f"{xml_size_in_mb:.2f}\n")
    texts.append(f"{total_files}\n")
    texts.append(f"{hms_duration}")
    texts.append(f"{total_duration:.2f})\n")
    texts.append(f"{size_in_mb:.2f}\n")
    texts.append(f"{source_files}\n")
    texts.append(f"{source_hms}\n")
    texts.append(f"{source_size_in_mb:.2f}\n")
    texts.append(f"{sub_files}\n")
    texts.append(f"{sub_hms}\n")
    texts.append(f"{sub_size_in_mb:.2f}\n")

    # with open(join_folder_path(parent_path(directory), f"{os.path.basename(directory)}_output.txt"), "w", encoding="utf-8") as f:
    #     # f.write(f"XML 파일 총 개수: {xml_files}\n")
    #     # f.write(f"XML 파일 총 용량: {xml_size_in_mb:.2f}MB\n")
    #     f.write(f"MP4 파일 총 개수: {total_files}\n")
    #     f.write(f"MP4 파일 총 길이: {hms_duration} (초 단위: {total_duration:.2f}초)\n")
    #     f.write(f"MP4 파일 총 용량: {size_in_mb:.2f}MB\n")
    #     f.write(f"MP4 파일 source 개수: {source_files}\n")
    #     f.write(f"MP4 파일 source 길이: {source_hms} (초 단위: {source_duration:.2f}초)\n")
    #     f.write(f"MP4 파일 source 용량: {source_size_in_mb:.2f}MB\n")
    #     f.write(f"MP4 파일 parts 개수: {sub_files}\n")
    #     f.write(f"MP4 파일 parts 길이: {sub_hms} (초 단위: {sub_duration:.2f}초)\n")
    #     f.write(f"MP4 파일 parts 용량: {sub_size_in_mb:.2f}MB\n")

    print(f"{directory} 폴더 통계가 저장되었습니다.")
    return total_files, total_duration, total_size, source_files, source_duration, source_size, sub_files, sub_duration, sub_size, txt_files, txt_size, mp3_files, mp3_duration, mp3_size, xml_files, xml_size

def run(yymmdd_folder_path=None, parent_yymmdd_path=None, speaker_folder_path=None, extension='mp4'):
    print('1. yymmdd folder\n2. "_processing\\speaker" folder\n3. "_final working\\yyyymm\\speaker" folder')
    select = strip_quotes(input('Enter select process : '))
    if select=='1':
        pass
    #     if not yymmdd_folder_path:
    #         yymmdd_folder_path = strip_quotes(input('Enter yymmdd folder path: '))
    #     # if not extension:
    #         # extension = strip_quotes(input('Enter target extension : '))
    #     process(yymmdd_folder_path)
    # elif select=='2':
    #     if not parent_yymmdd_path:
    #         parent_yymmdd_path = strip_quotes(input("Enter parent of yymmdd folder : "))
    #     yymmdd_folders = get_subdirectories(parent_yymmdd_path)
    #     print(yymmdd_folders)
    #     texts = []
    #     for i, folder in enumerate(yymmdd_folders):
    #         json_data = process(folder)
    #         texts.append(json_data)
    #     parts_total = None
    #     parts_length = None
    #     parts_size = None
    #     parts_duration = None
    #     for i, json_data in enumerate(texts):
    #         if i==0:
    #             parts_total = float(texts[i]['sub_files']['__text__'])
    #             parts_size = float(texts[i]['sub_size_in_mb']['__text__'])
    #             parts_duration = float(texts[i]['sub_duration']['__text__'])
    #             continue
            
    #         parts_total += float(texts[i]['sub_files']['__text__'])
    #         parts_size += float(texts[i]['sub_size_in_mb']['__text__'])
    #         parts_duration += float(texts[i]['sub_duration']['__text__'])
    #     parts_length = seconds_to_hms(parts_duration)
    #     with open(join_folder_path(parent_yymmdd_path, f"{os.path.basename(parent_yymmdd_path)}_output2.txt"), "w", encoding="utf-8") as f:
    #         f.write(f"MP4 파일 parts 총개수: {parts_total}\n")
    #         f.write(f"MP4 파일 parts 총길이: {parts_length} (초 단위: {parts_duration:.2f}초)\n")
    #         f.write(f"MP4 파일 parts 총용량: {parts_size:.2f}MB\n")
    elif select=='3':
        speaker_folder_path = speaker_folder_path or strip_quotes(input("Enter speaker folder : "))
        # print(speaker_folders)
        total_files, total_duration, total_size, source_files, source_duration, source_size, sub_files, sub_duration, sub_size, txt_files, txt_size, mp3_files, mp3_duration, mp3_size, xml_files, xml_size = process(speaker_folder_path)
        print("Result coming soon.")
        txt_file_path = join_folder_path(parent_path(speaker_folder_path), f"speaker_output.txt")
        with open(txt_file_path, "w", encoding="utf-8") as f:
            # f.write(f"MP4 파일 parts 총개수: {parts_total}\n")
            # f.write(f"MP4 파일 parts 총길이: {parts_length} (초 단위: {parts_duration:.2f}초)\n")
            # f.write(f"MP4 파일 parts 총용량: {parts_size:.2f}MB\n")
            f.write(f"MP4 파일 parts 총개수: {sub_files}\n")
            f.write(f"MP4 파일 parts 총길이: {seconds_to_hms(sub_duration)} (초 단위: {sub_duration:.2f}초)\n")
            f.write(f"MP4 파일 parts 총용량: {(sub_size / (1024 * 1024)):.2f}MB\n")
            f.write(f"MP3 파일 총개수: {mp3_files}\n")
            f.write(f"MP3 파일 총길이: {seconds_to_hms(mp3_duration)} (초 단위: {mp3_duration:.2f}초)\n")
            f.write(f"MP3 파일 총용량: {(mp3_size / (1024 * 1024)):.2f}MB\n")
            f.write(f"txt 파일 총개수: {txt_files}\n")
            f.write(f"txt 파일 총용량: {(txt_size):.2f}KB\n")
            f.write(f"xml 파일 총개수: {xml_files}\n")
            f.write(f"xml 파일 총용량: {(xml_size):.2f}KB\n")
        print(f"MP4 파일 parts 총개수: {sub_files}")
        print(f"MP4 파일 parts 총길이: {seconds_to_hms(sub_duration)} (초 단위: {sub_duration:.2f}초)")
        print(f"MP4 파일 parts 총용량: {(sub_size / (1024 * 1024)):.2f}MB")
        print(f"MP3 파일 총개수: {mp3_files}")
        print(f"MP3 파일 총길이: {seconds_to_hms(mp3_duration)} (초 단위: {mp3_duration:.2f}초)")
        print(f"MP3 파일 총용량: {(mp3_size / (1024 * 1024)):.2f}MB")
        print(f"txt 파일 총개수: {txt_files}")
        print(f"txt 파일 총용량: {(txt_size):.2f}KB")
        print(f"xml 파일 총개수: {xml_files}")
        print(f"xml 파일 총용량: {(xml_size):.2f}KB")
        print("Done!")
        speaker_folder_path = None

    yymmdd_folder_path = None

if __name__ == "__main__":
    run()