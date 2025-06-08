"""
파일 시스템 모니터링을 위한 핸들러 클래스
"""
import os
import time
from typing import Callable, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FolderWatchdog(FileSystemEventHandler):
    """파일 시스템 모니터링을 위한 핸들러 클래스"""
    
    def __init__(self, target_path: str, action: Optional[Callable] = None, time_interval: int = 1):
        """
        FolderWatchdog 초기화
        
        Args:
            target_path (str): 모니터링할 폴더 경로
            action (Callable, optional): 파일 변경 시 실행할 콜백 함수
            time_interval (int): 모니터링 간격 (초)
        """
        self.target_path = target_path
        self.action = action
        self.time_interval = self._validate_time_interval(time_interval)
        self.observer = None
        self.is_running = False
    
    def start(self) -> None:
        """모니터링을 시작합니다."""
        if not self.is_running:
            self.observer = Observer()
            self.observer.schedule(self, path=self.target_path, recursive=True)
            self.observer.start()
            self.is_running = True
    
    def stop(self) -> None:
        """모니터링을 중지합니다."""
        if self.is_running and self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.is_running = False
    
    def pause(self) -> None:
        """모니터링을 일시 중지합니다."""
        self.stop()
    
    def resume(self) -> None:
        """일시 중지된 모니터링을 재개합니다."""
        self.start()
    
    def set_action(self, action: Callable) -> None:
        """
        파일 변경 시 실행할 콜백 함수를 설정합니다.
        
        Args:
            action (Callable): 실행할 콜백 함수
        """
        self.action = action
    
    def on_modified(self, event) -> None:
        """
        파일이 수정되었을 때 호출되는 메서드
        
        Args:
            event: 파일 시스템 이벤트
        """
        if not event.is_directory and self.action:
            self.action()
    
    def _validate_time_interval(self, time_interval: int) -> int:
        """
        시간 간격을 검증합니다.
        
        Args:
            time_interval (int): 검증할 시간 간격
            
        Returns:
            int: 검증된 시간 간격
            
        Raises:
            ValueError: 유효하지 않은 시간 간격이 입력된 경우
        """
        try:
            time_interval = int(time_interval)
            if time_interval < 1:
                raise ValueError("시간 간격은 1초 이상이어야 합니다.")
            return time_interval
        except (ValueError, TypeError):
            raise ValueError("유효한 시간 간격(초)을 입력해주세요.")
    
    def run(self) -> None:
        """모니터링을 시작하고 계속 실행합니다."""
        self.start()
        try:
            while self.is_running:
                time.sleep(self.time_interval)
        except KeyboardInterrupt:
            self.stop()

if __name__ == "__main__":
    def test_action():
        print("파일이 수정되었습니다!")
    
    # 테스트 경로 설정
    test_path = input("모니터링할 폴더 경로를 입력하세요: ")
    interval = input("모니터링 간격(초)을 입력하세요 (기본값: 1): ") or "1"
    
    # 핸들러 생성 및 실행
    watchdog = FolderWatchdog(test_path, action=test_action, time_interval=int(interval))
    print(f"'{test_path}' 폴더 모니터링을 시작합니다...")
    watchdog.run() 