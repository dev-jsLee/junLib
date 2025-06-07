"""
비디오 파일 처리를 위한 핸들러 클래스
"""
import os
from moviepy.editor import VideoFileClip, AudioFileClip

class VideoHandler:
    """비디오 파일 처리를 위한 핸들러 클래스"""
    
    def __init__(self, file_path=None):
        """
        Args:
            file_path (str, optional): 비디오 파일 경로
        """
        self.file_path = file_path
        self.clip = None
        if file_path:
            self.load(file_path)
    
    def load(self, file_path):
        """비디오 파일을 로드합니다."""
        self.file_path = file_path
        self.clip = VideoFileClip(file_path)
        return self
    
    def get_duration(self):
        """비디오 길이를 반환합니다."""
        if self.clip:
            return float(self.clip.duration)
        return None
    
    def close(self):
        """비디오 클립을 닫습니다."""
        if self.clip:
            self.clip.close()
            self.clip = None
        return self

class AudioHandler:
    """오디오 파일 처리를 위한 핸들러 클래스"""
    
    def __init__(self, file_path=None):
        """
        Args:
            file_path (str, optional): 오디오 파일 경로
        """
        self.file_path = file_path
        self.clip = None
        if file_path:
            self.load(file_path)
    
    def load(self, file_path):
        """오디오 파일을 로드합니다."""
        self.file_path = file_path
        self.clip = AudioFileClip(file_path)
        return self
    
    def get_duration(self):
        """오디오 길이를 반환합니다."""
        if self.clip:
            return float(self.clip.duration)
        return None
    
    def close(self):
        """오디오 클립을 닫습니다."""
        if self.clip:
            self.clip.close()
            self.clip = None
        return self 