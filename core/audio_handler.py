"""
비디오 파일 처리를 위한 핸들러 클래스
"""
import os
import sys
import csv
from . import junLib

# moviepy 임포트
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy import VideoFileClip, AudioFileClip

class VideoHandler:
    """비디오 파일을 처리하기 위한 핸들러 클래스"""
    
    def __init__(self, video_path='') -> None:
        """
        VideoHandler 초기화
        
        Args:
            video_path (str, optional): 비디오 파일 경로. 기본값은 빈 문자열.
        """
        if video_path:
            self.set_video(video_path)

    def set_video(self, video_path=''):
        """
        비디오 파일 경로 설정
        
        Args:
            video_path (str, optional): 비디오 파일 경로. 기본값은 빈 문자열.
            
        Returns:
            VideoHandler: 체이닝을 위한 self 반환
        """
        self.video_path = video_path or junLib.strip_quotes(input("Enter video file path : "))
        return self

    def get_duration(self):
        """
        비디오 파일의 재생 시간을 초 단위로 반환
        
        Returns:
            float: 비디오 재생 시간(초)
        """
        clip = VideoFileClip(self.video_path)
        self.duration = float(clip.duration)
        clip.close()
        return self.duration

def get_files_info_mp4(folder_path, show_msg:bool=False):
    """
    폴더 내의 모든 MP4 파일 정보를 수집
    
    Args:
        folder_path (str): MP4 파일이 있는 폴더 경로
        show_msg (bool, optional): 진행 상황 메시지 표시 여부. 기본값은 False.
        
    Returns:
        tuple: (파일 수, 총 파일 크기(바이트), 총 재생 시간(초))
    """
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
        self.audio_path = video_path or junLib.strip_quotes(input("Enter video file path : "))
        return self

    def get_duration(self):
        clip = AudioFileClip(self.audio_path)
        self.duration = float(clip.duration)
        clip.close
        return (self.duration)

if __name__ == "__main__":
    obj = VideoHandler()
    video_file_path = junLib.strip_quotes(input("Enter video file path : "))
    obj.set_video(video_file_path)
    print(obj.get_duration())