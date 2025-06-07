import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *
from moviepy.editor import VideoFileClip

def get_video_lengths(folder):
    result = ""
    total_duration = 0
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".mp4"):
                file_path = os.path.join(root, file)
                try:
                    clip = VideoFileClip(file_path)
                    duration = clip.duration
                    clip.close()
                    total_duration += duration
                    result += f"{file} : {duration} seconds\n"
                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")
    return result, total_duration

def open_write(content, file_path):
    with open(file_path, "w") as f:
        f.write(content)

def open_append(content, file_path):
    with open(file_path, "a") as f:
        f.write(content)

def run_subdir(folder_path):
    if not folder_path:
        folder_path = strip_quotes(input("폴더 경로를 입력하세요: "))
    actual_total = 0
    output_text = ""
    real_output_file_path = ""
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            subdir = os.path.join(root, dir)
            video_lengths, total_length = get_video_lengths(subdir)
            if video_lengths:
                real_output_file_path = os.path.join(os.path.dirname(root), '_' + os.path.basename(root) + '_total.txt')
                # split = split_str(str(total_length), split_code='.')
                total_length = cut_after_dot(total_length, length_after_dot=2)
                output_text += make_output_line(os.path.basename(subdir), total_length)
                # save_to_file(output_text, str(real_output_file_path))
                # print(f"결과가 {real_output_file_path}에 저장되었습니다.")
                actual_total += float(total_length)
    actual_total = cut_after_dot(actual_total, length_after_dot=2)

    output_text += make_output_line('actual_total', actual_total)
    if real_output_file_path:
        open_write(output_text, str(real_output_file_path))
        print(f"결과가 {real_output_file_path}에 저장되었습니다.")
        return real_output_file_path
    else:
        return None

def make_output_line(text, time_seconds):
    time_minute = cut_after_dot(str(float(time_seconds)/60), length_after_dot=2)
    return str(text) + '\t' + str(time_seconds) + '\t' + str(time_minute) + '\n'

def run():
    folder_path = strip_quotes(input("폴더 경로를 입력하세요: "))
    subdir = path_func(os.path.join(folder_path, os.path.basename(folder_path)))
    output_file_path = subdir.rename(suffix='_total', ext='txt')

    video_lengths = get_video_lengths(folder_path)
    open_write(video_lengths, output_file_path)
    print(f"결과가 {output_file_path}에 저장되었습니다.")

if __name__ == "__main__":
    # run()
    run_subdir()