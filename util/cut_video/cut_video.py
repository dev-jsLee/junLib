# cut_video.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

class cut_time_by_time():
    video_path=None
    def __init__(self, video_path=None, audio_path=None) -> None:
        if video_path:
            self.video_path = video_path
        elif audio_path:
            self.audio_path = audio_path

    def cut_video_time_no_stamp(self, start_second, end_second, output_path=None):
        base_path = os.path.dirname(self.video_path)
        file_name, file_ext = os.path.splitext(os.path.basename(self.video_path))
        split_file_name = str(file_name).split('_')
        # origin_start = float(split_file_name[0])
        # origin_end = float(split_file_name[1])
        # real_start = origin_start + float(start_second)
        # real_end = origin_start+float(end_second)
        start_time_str = str(start_second).zfill(5)
        end_time_str = str(end_second).zfill(5)
        output_file_with_times = f"{start_time_str}_{end_time_str}{file_ext}"
        output_path = os.path.join(base_path, output_file_with_times) if not output_path else output_path
        # create_folder_if_not_exists(os.path.join(base_path, file_name))
        ffmpeg_extract_subclip(self.video_path, (float(start_second)), (float(end_second)), targetname=output_path)
        print(f"Video cut and saved as '{os.path.basename(output_path)}'")

    def cut_video_time(self, start_second, end_second):
        base_path = os.path.dirname(self.video_path)
        file_name, file_ext = os.path.splitext(os.path.basename(self.video_path))
        split_file_name = str(file_name).split('_')
        origin_start = float(split_file_name[0])
        origin_end = float(split_file_name[1])
        real_start = origin_start + float(start_second)
        real_end = origin_start+float(end_second)
        start_time_str = str(real_start).zfill(5)
        end_time_str = str(real_end).zfill(5)
        output_file_with_times = f"{start_time_str}_{end_time_str}{file_ext}"
        output_path = os.path.join(base_path, output_file_with_times)
        # create_folder_if_not_exists(os.path.join(base_path, file_name))
        ffmpeg_extract_subclip(self.video_path, int(float(start_second)), int(float(end_second)), targetname=output_path)
        print(f"Video cut and saved as '{output_file_with_times}'")

def run():
    video_path = strip_quotes(input('Drag and Drop Video Source File: '))
    obj = cut_time_by_time(video_path=video_path)
    info = []
    flag = True
    while(flag):
        print('if you want to be done process, Enter empty')
        start_time = strip_quotes(input('Enter Start seconds of the video'))
        end_time = strip_quotes(input('Enter End seconds of the video'))
        if not start_time or not end_time:
            flag = False
            continue
        info.append({'start': start_time, 'end': end_time})
    for i in range(len(info)):
        obj.cut_video_time(start_second=info[i]['start'], end_second=info[i]['end'])
    print('done process')

def run_no_timestamp():
    video_path = strip_quotes(input('Drag and Drop Video Source File: '))
    obj = cut_time_by_time(video_path=video_path)
    flag = True
    while(flag):
        print('if you want to be done process, Enter empty')
        start_time = strip_quotes(input('Enter Start seconds of the video : '))
        end_time = strip_quotes(input('Enter End seconds of the video : '))
        if not start_time or not end_time:
            flag = False
            continue
        obj.cut_video_time_no_stamp(start_second=start_time, end_second=end_time)
        print('done process')
if __name__=='__main__':
    run_no_timestamp()