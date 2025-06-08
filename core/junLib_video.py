import os
import sys
import csv
from junLib import strip_quotes

# moviepy 임포트
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy import VideoFileClip, AudioFileClip

class video_lib():
    
    def __init__(self, video_path='') -> None:
        if video_path:
            self.set_video(video_path)
        pass

    def set_video(self, video_path=''):
        self.video_path = video_path or strip_quotes(input("Enter video file path : "))
        return self

    def get_duration(self):
        clip = VideoFileClip(self.video_path)
        self.duration = float(clip.duration)
        clip.close
        return self.duration

def get_files_info_mp4(folder_path, show_msg:bool=False):
    mp4_count = 0
    mp4_size = 0
    mp4_length = 0
    files = junLib.get_files_path_in_folder_via_ext(folder_path, 'mp4')
    for i, file in enumerate(files, 1):
        if show_msg and (i % 10 == 0 or i == len(files)):
            print(f"file : {i}/{len(files)}")
        try:
            clip = VideoFileClip(file)
            mp4_length += clip.duration
            clip.close()
        except Exception:
            pass
        finally:
            mp4_count += 1
            file_size = os.path.getsize(file)
            mp4_size += file_size
    return mp4_count, mp4_size, mp4_length

class audio_lib():
    def __init__(self, audio_path='') -> None:
        if audio_path:
            self.set_audio(audio_path)

    def set_audio(self, video_path=''):
        self.audio_path = video_path or strip_quotes(input("Enter video file path : "))
        return self

    def get_duration(self):
        clip = AudioFileClip(self.audio_path)
        self.duration = float(clip.duration)
        clip.close
        return (self.duration)

if __name__ == "__main__":
    obj = video_lib()
    video_file_path = strip_quotes(input("Enter video file path : "))
    obj.set_video(video_file_path)
    print(obj.get_duration())