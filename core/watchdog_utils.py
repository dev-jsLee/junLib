"""
파일 시스템 모니터링을 위한 유틸리티 함수들
"""
import os
import time
from typing import Callable, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def create_file_handler(action: Callable) -> FileSystemEventHandler:
    """
    파일 변경 이벤트를 처리할 핸들러를 생성합니다.
    
    Args:
        action (Callable): 파일 변경 시 실행할 콜백 함수
        
    Returns:
        FileSystemEventHandler: 생성된 이벤트 핸들러
    """
    class FileHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if not event.is_directory:
                action()
    
    return FileHandler()

def watch_folder(folder_path: str, action: Callable, recursive: bool = True) -> Observer:
    """
    폴더를 모니터링하는 Observer를 생성하고 시작합니다.
    
    Args:
        folder_path (str): 모니터링할 폴더 경로
        action (Callable): 파일 변경 시 실행할 콜백 함수
        recursive (bool): 하위 폴더도 모니터링할지 여부
        
    Returns:
        Observer: 생성된 Observer 객체
    """
    event_handler = create_file_handler(action)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=recursive)
    observer.start()
    return observer

def stop_observer(observer: Observer) -> None:
    """
    Observer를 중지합니다.
    
    Args:
        observer (Observer): 중지할 Observer 객체
    """
    observer.stop()
    observer.join()

def watch_folder_with_interval(folder_path: str, action: Callable, 
                             interval: int = 1, recursive: bool = True) -> None:
    """
    지정된 간격으로 폴더를 모니터링합니다.
    
    Args:
        folder_path (str): 모니터링할 폴더 경로
        action (Callable): 파일 변경 시 실행할 콜백 함수
        interval (int): 모니터링 간격 (초)
        recursive (bool): 하위 폴더도 모니터링할지 여부
    """
    observer = watch_folder(folder_path, action, recursive)
    try:
        while True:
            time.sleep(interval)
    except KeyboardInterrupt:
        stop_observer(observer)

if __name__ == "__main__":
    def test_action():
        print("파일이 수정되었습니다!")
    
    # 테스트 경로 설정
    test_path = input("모니터링할 폴더 경로를 입력하세요: ")
    interval = input("모니터링 간격(초)을 입력하세요 (기본값: 1): ") or "1"
    recursive = input("하위 폴더도 모니터링할까요? (y/n, 기본값: y): ").lower() != 'n'
    
    print(f"'{test_path}' 폴더 모니터링을 시작합니다...")
    watch_folder_with_interval(
        test_path,
        action=test_action,
        interval=int(interval),
        recursive=recursive
    ) 