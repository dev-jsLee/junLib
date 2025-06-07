"""
비디오 파일 처리를 위한 모듈

이 모듈은 비디오와 오디오 파일을 처리하기 위한 클래스와 유틸리티 함수들을 제공합니다.
"""

from .VideoHandler import VideoHandler, get_files_info_mp4
from .AudioHandler import AudioHandler, EmotionTaggingApp

__all__ = [
    'VideoHandler',
    'AudioHandler',
    'EmotionTaggingApp',
    'get_files_info_mp4'
]
