"""
비디오/오디오 파일 처리를 위한 유틸리티 함수들
"""
import os
from typing import Tuple, List
from moviepy import VideoFileClip, AudioFileClip
from file_utils import path_exist, get_files_path_in_folder_via_ext

def get_video_duration(file_path: str) -> float:
    """
    비디오 파일의 길이를 반환합니다.
    
    Args:
        file_path (str): 비디오 파일 경로
        
    Returns:
        float: 비디오 길이(초)
        
    Raises:
        FileNotFoundError: 파일이 존재하지 않을 때
        Exception: 비디오 파일 로드 중 오류 발생 시
    """
    if not path_exist(file_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        
    clip = VideoFileClip(file_path)
    try:
        return float(clip.duration)
    finally:
        clip.close()

def get_audio_duration(file_path: str) -> float:
    """
    오디오 파일의 길이를 반환합니다.
    
    Args:
        file_path (str): 오디오 파일 경로
        
    Returns:
        float: 오디오 길이(초)
        
    Raises:
        FileNotFoundError: 파일이 존재하지 않을 때
        Exception: 오디오 파일 로드 중 오류 발생 시
    """
    if not path_exist(file_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        
    clip = AudioFileClip(file_path)
    try:
        return float(clip.duration)
    finally:
        clip.close()

def get_mp4_files_info(folder_path: str, show_progress: bool = False) -> Tuple[int, int, float]:
    """
    폴더 내의 MP4 파일들의 정보를 수집합니다.
    
    Args:
        folder_path (str): 폴더 경로
        show_progress (bool): 진행 상황 표시 여부
        
    Returns:
        Tuple[int, int, float]: (파일 수, 총 파일 크기(바이트), 총 재생 시간(초))
        
    Raises:
        FileNotFoundError: 폴더가 존재하지 않을 때
    """
    if not path_exist(folder_path):
        raise FileNotFoundError(f"폴더를 찾을 수 없습니다: {folder_path}")
        
    mp4_count = 0
    mp4_size = 0
    mp4_length = 0
    
    files = get_files_path_in_folder_via_ext(folder_path, 'mp4')
    total_files = len(files)
    
    for i, file in enumerate(files, 1):
        if show_progress and (i % 10 == 0 or i == total_files):
            print(f"파일 처리 중: {i}/{total_files}")
            
        try:
            clip = VideoFileClip(file)
            mp4_length += clip.duration
            clip.close()
        except Exception as e:
            print(f"파일 처리 중 오류 발생 ({file}): {str(e)}")
        finally:
            mp4_count += 1
            file_size = os.path.getsize(file)
            mp4_size += file_size
            
    return mp4_count, mp4_size, mp4_length

def extract_subclip(video_path: str, output_path: str, start_time: float, end_time: float) -> bool:
    """
    비디오 파일에서 일부분을 추출합니다.
    
    Args:
        video_path (str): 입력 비디오 파일 경로
        output_path (str): 출력 비디오 파일 경로
        start_time (float): 시작 시간(초)
        end_time (float): 종료 시간(초)
        
    Returns:
        bool: 추출 성공 여부
        
    Raises:
        FileNotFoundError: 입력 파일이 존재하지 않을 때
        Exception: 추출 중 오류 발생 시
    """
    if not path_exist(video_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {video_path}")
        
    try:
        from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
        ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=output_path)
        return True
    except Exception as e:
        print(f"비디오 추출 중 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        # 테스트용 비디오 파일 경로
        test_video = input("테스트할 비디오 파일 경로를 입력하세요: ").strip('"')
        
        # 비디오 길이 테스트
        duration = get_video_duration(test_video)
        print(f"비디오 길이: {duration:.2f}초")
        
        # 폴더 내 MP4 파일 정보 테스트
        folder_path = os.path.dirname(test_video)
        count, size, length = get_mp4_files_info(folder_path, show_progress=True)
        print(f"\n폴더 내 MP4 파일 정보:")
        print(f"파일 수: {count}")
        print(f"총 크기: {size / (1024*1024):.2f}MB")
        print(f"총 재생 시간: {length / 60:.2f}분")
        
    except Exception as e:
        print(f"오류 발생: {str(e)}") 