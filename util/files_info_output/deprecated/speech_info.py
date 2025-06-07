import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *
from moviepy.editor import VideoFileClip
from _workplace.util.files_info_output import speaker_info_deprecated as info

def get_size_in_kb(size_in_bytes):
    return size_in_bytes / 1024

def get_size_in_mb(size_in_bytes):
    return size_in_bytes / (1024 * 1024)

def get_mp4_statistics(folder_path):
    # folders = sub_path(folder_path)
    mp4_count = 0
    mp4_size = 0
    mp4_length = 0
    # for folder_path in folders:
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()

            if file_extension == ".mp4":
                mp4_count += 1
                file_size = os.path.getsize(file_path)
                mp4_size += file_size
                try:
                    clip = VideoFileClip(file_path)
                    mp4_length += clip.duration
                    clip.close()
                except Exception:
                    pass

    return mp4_count, mp4_size, mp4_length

def get_xml_statistics(folder_path):
    xml_count = 0
    xml_size = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()

            if file_extension == ".xml":
                xml_count += 1
                xml_size += os.path.getsize(file_path)

    return xml_count, xml_size

def get_jpg_statistics(folder_path):
    jpg_count = 0
    jpg_size = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()

            if file_extension == ".jpg":
                jpg_count += 1
                jpg_size += os.path.getsize(file_path)

    return jpg_count, jpg_size

def run(folder_path):
    mp4_count, mp4_size, mp4_length = get_mp4_statistics(folder_path)
    xml_count, xml_size = get_xml_statistics(folder_path)
    jpg_count, jpg_size = get_jpg_statistics(folder_path)
    default_output_path = os.path.join(parent_path(folder_path), os.path.basename(folder_path) + "_output.txt")

    hms_duration = info.seconds_to_hms(mp4_length)
    
    # MP4 결과 출력
    mp4_output_file = os.path.join(folder_path, "output_mp4.txt")
    with open(default_output_path, "w") as f:
        if mp4_count > 0:
            f.write(f"MP4 Statistics:\n")
            f.write(f"Total count:\t{mp4_count}\n")
            f.write(f"Total size:\t{get_size_in_kb(mp4_size):.2f} KB\t({get_size_in_mb(mp4_size):.2f} MB)\n")
            f.write(f"Total length:\t{mp4_length:.2f} seconds\t{hms_duration}\n\n")

    # XML 결과 출력
    # xml_output_file = os.path.join(folder_path, "output_xml.txt")
    # with open(default_output_path, "w") as f:
        if xml_count > 0:
            f.write(f"XML Statistics:\n")
            f.write(f"Total count:\t{xml_count}\n")
            f.write(f"Total size:\t{get_size_in_kb(xml_size):.2f} KB\t({get_size_in_mb(xml_size):.2f} MB)\n\n")

    # JPG 결과 출력
    # jpg_output_file = os.path.join(folder_path, "output_jpg.txt")
    # with open(default_output_path, "w") as f:
        if jpg_count > 0:
            f.write(f"JPG Statistics:\n")
            f.write(f"Total count:\t{jpg_count}\n")
            f.write(f"Total size:\t{get_size_in_kb(jpg_size):.2f} KB\t({get_size_in_mb(jpg_size):.2f} MB)\n\n")

if __name__ == "__main__":
    while(True):
        folder_path = strip_quotes(input("폴더 경로를 입력하세요: "))
        run(folder_path)
