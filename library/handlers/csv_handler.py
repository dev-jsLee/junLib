"""
CSV 파일 처리를 위한 핸들러 클래스
"""
import os
import csv
import pandas as pd

class CSVHandler:
    """CSV 파일 처리를 위한 핸들러 클래스"""
    
    def __init__(self, file_path=None):
        """
        Args:
            file_path (str, optional): CSV 파일 경로
        """
        self.file_path = file_path
        self.data = None
        if file_path:
            self.load(file_path)
    
    def load(self, file_path):
        """CSV 파일을 로드합니다."""
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        return self
    
    def save(self, file_path=None, index=False):
        """CSV 파일을 저장합니다."""
        if file_path:
            self.file_path = file_path
        if self.data is not None:
            self.data.to_csv(self.file_path, index=index)
        return self
    
    def get_data(self):
        """데이터를 반환합니다."""
        return self.data
    
    def set_data(self, data):
        """데이터를 설정합니다."""
        self.data = data
        return self 