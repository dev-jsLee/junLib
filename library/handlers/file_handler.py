"""
파일 시스템 처리를 위한 핸들러 클래스
"""
import os
import shutil
import subprocess

class FileHandler:
    """파일 시스템 처리를 위한 핸들러 클래스"""
    
    def __init__(self, file_path=None):
        """
        Args:
            file_path (str, optional): 파일 경로
        """
        self.file_path = file_path
    
    def exists(self):
        """파일이 존재하는지 확인합니다."""
        return os.path.exists(self.file_path)
    
    def create_folder(self, folder_path=None):
        """폴더를 생성합니다."""
        path = folder_path or self.file_path
        if not os.path.exists(path):
            os.makedirs(path)
        return self
    
    def move_file(self, target_path, show_msg=False):
        """파일을 이동합니다."""
        try:
            shutil.move(self.file_path, target_path)
            if show_msg:
                print(f"파일을 이동했습니다: {self.file_path} -> {target_path}")
        except Exception as e:
            print(f"파일 이동 중 오류 발생: {e}")
        return self
    
    def copy_file(self, target_path, show_msg=False):
        """파일을 복사합니다."""
        try:
            shutil.copy2(self.file_path, target_path)
            if show_msg:
                print(f"파일을 복사했습니다: {self.file_path} -> {target_path}")
        except Exception as e:
            print(f"파일 복사 중 오류 발생: {e}")
        return self
    
    def delete_file(self, show_msg=False):
        """파일을 삭제합니다."""
        try:
            os.remove(self.file_path)
            if show_msg:
                print(f"파일을 삭제했습니다: {self.file_path}")
        except Exception as e:
            print(f"파일 삭제 중 오류 발생: {e}")
        return self
    
    def get_files_in_folder(self, extension=None, recursive=False):
        """폴더 내의 파일 목록을 반환합니다."""
        files = []
        for root, _, filenames in os.walk(self.file_path):
            for filename in filenames:
                if extension and not filename.endswith(extension):
                    continue
                files.append(os.path.join(root, filename))
            if not recursive:
                break
        return files 