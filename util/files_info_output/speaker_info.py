# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from _workplace.library.junLib import *
import moviepy.editor as mp
def get_directory_xml_stats(directory):
    total_files = 0
    total_size = 0  # in bytes

    # List files in the given directory
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
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

    return total_files, total_duration, total_size

def get_subfolder_mp4_stats(directory):
    total_files = 0
    total_duration = 0  # in seconds
    total_size = 0  # in bytes

    # Walk through directory and subdirectories
    for dirpath, dirnames, filenames in os.walk(directory):
        # Skip the root directory
        if dirpath == directory:
            continue

        for filename in filenames:
            if filename.endswith('.mp4'):
                total_files += 1
                filepath = os.path.join(dirpath, filename)
                
                # Get duration of the video
                clip = mp.VideoFileClip(filepath)
                total_duration += clip.duration
                
                # Get size of the file
                total_size += os.path.getsize(filepath)

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
    xml_files, xml_size = get_directory_xml_stats(directory)
    # Convert total_duration to hours:minutes:seconds format
    hms_duration = seconds_to_hms(total_duration)
    sub_hms = seconds_to_hms(sub_duration)
    source_hms = seconds_to_hms(source_duration)

    # Convert total_size to MB
    size_in_mb = total_size / (1024 * 1024)
    sub_size_in_mb = sub_size / (1024 * 1024)
    source_size_in_mb = source_size / (1024 * 1024)
    xml_size_in_mb = xml_size / (1024 * 1024)

    with open(join_folder_path(parent_path(directory), f"{os.path.basename(directory)}_output.txt"), "w", encoding="utf-8") as f:
        f.write(f"XML 파일 총 개수: {xml_files}\n")
        f.write(f"XML 파일 총 용량: {xml_size_in_mb:.2f}MB\n")
        f.write(f"MP4 파일 총 개수: {total_files}\n")
        f.write(f"MP4 파일 총 길이: {hms_duration} (초 단위: {total_duration:.2f}초)\n")
        f.write(f"MP4 파일 총 용량: {size_in_mb:.2f}MB\n")
        f.write(f"MP4 파일 source 개수: {source_files}\n")
        f.write(f"MP4 파일 source 길이: {source_hms} (초 단위: {source_duration:.2f}초)\n")
        f.write(f"MP4 파일 source 용량: {source_size_in_mb:.2f}MB\n")
        f.write(f"MP4 파일 parts 개수: {sub_files}\n")
        f.write(f"MP4 파일 parts 길이: {sub_hms} (초 단위: {sub_duration:.2f}초)\n")
        f.write(f"MP4 파일 parts 용량: {sub_size_in_mb:.2f}MB\n")

    print(f"통계가 {join_folder_path(parent_path(directory), 'speaker_stats.txt')} 파일에 저장되었습니다.")

def run(parent_folder_path=None, extension='mp4'):
    if not parent_folder_path:
        parent_folder_path = strip_quotes(input('Enter speaker folder path: '))
    if not extension:
        extension = strip_quotes(input('Enter target extension : '))
    process(parent_folder_path)
    parent_folder_path = None

if __name__ == "__main__":
    run()