"""
비디오/오디오 파일 처리를 위한 핸들러 클래스
"""
import os
from typing import Optional, Tuple
from moviepy import VideoFileClip, AudioFileClip
from file_utils import path_exist
from video_utils import get_video_duration, get_audio_duration, extract_subclip

class VideoHandler:
    """비디오 파일 처리를 위한 핸들러 클래스"""
    
    def __init__(self, file_path: Optional[str] = None) -> None:
        """
        Args:
            file_path (str, optional): 비디오 파일 경로
        """
        self.file_path = file_path
        self.clip = None
        if file_path:
            self.load(file_path)
    
    def load(self, file_path: str) -> 'VideoHandler':
        """
        비디오 파일을 로드합니다.
        
        Args:
            file_path (str): 비디오 파일 경로
            
        Returns:
            VideoHandler: 체이닝을 위한 self 반환
            
        Raises:
            FileNotFoundError: 파일이 존재하지 않을 때
        """
        if not path_exist(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
            
        self.file_path = file_path
        self.clip = VideoFileClip(file_path)
        return self
    
    def get_duration(self) -> Optional[float]:
        """
        비디오 길이를 반환합니다.
        
        Returns:
            Optional[float]: 비디오 길이(초) (로드되지 않은 경우 None)
        """
        if not self.file_path:
            return None
        return get_video_duration(self.file_path)
    
    def extract_subclip(self, output_path: str, start_time: float, end_time: float) -> bool:
        """
        비디오 파일에서 일부분을 추출합니다.
        
        Args:
            output_path (str): 출력 비디오 파일 경로
            start_time (float): 시작 시간(초)
            end_time (float): 종료 시간(초)
            
        Returns:
            bool: 추출 성공 여부
        """
        if not self.file_path:
            raise ValueError("비디오 파일이 로드되지 않았습니다.")
        return extract_subclip(self.file_path, output_path, start_time, end_time)
    
    def close(self) -> 'VideoHandler':
        """
        비디오 클립을 닫습니다.
        
        Returns:
            VideoHandler: 체이닝을 위한 self 반환
        """
        if self.clip:
            self.clip.close()
            self.clip = None
        return self

class AudioHandler:
    """오디오 파일 처리를 위한 핸들러 클래스"""
    
    def __init__(self, file_path: Optional[str] = None) -> None:
        """
        Args:
            file_path (str, optional): 오디오 파일 경로
        """
        self.file_path = file_path
        self.clip = None
        if file_path:
            self.load(file_path)
    
    def load(self, file_path: str) -> 'AudioHandler':
        """
        오디오 파일을 로드합니다.
        
        Args:
            file_path (str): 오디오 파일 경로
            
        Returns:
            AudioHandler: 체이닝을 위한 self 반환
            
        Raises:
            FileNotFoundError: 파일이 존재하지 않을 때
        """
        if not path_exist(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
            
        self.file_path = file_path
        self.clip = AudioFileClip(file_path)
        return self
    
    def get_duration(self) -> Optional[float]:
        """
        오디오 길이를 반환합니다.
        
        Returns:
            Optional[float]: 오디오 길이(초) (로드되지 않은 경우 None)
        """
        if not self.file_path:
            return None
        return get_audio_duration(self.file_path)
    
    def close(self) -> 'AudioHandler':
        """
        오디오 클립을 닫습니다.
        
        Returns:
            AudioHandler: 체이닝을 위한 self 반환
        """
        if self.clip:
            self.clip.close()
            self.clip = None
        return self

if __name__ == "__main__":
    try:
        # 테스트용 비디오 파일 경로
        test_video = input("테스트할 비디오 파일 경로를 입력하세요: ").strip('"')
        
        # 비디오 핸들러 테스트
        video_handler = VideoHandler(test_video)
        print(f"비디오 길이: {video_handler.get_duration():.2f}초")
        
        # 오디오 핸들러 테스트
        audio_handler = AudioHandler(test_video)
        print(f"오디오 길이: {audio_handler.get_duration():.2f}초")
        
        # 리소스 정리
        video_handler.close()
        audio_handler.close()
        
    except Exception as e:
        print(f"오류 발생: {str(e)}") 