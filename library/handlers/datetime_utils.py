"""
날짜/시간 처리를 위한 유틸리티 함수들
"""
from datetime import datetime, timedelta

def format_time(seconds):
    """초를 HH:MM:SS 형식으로 변환합니다."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def format_time_with_ms(seconds):
    """초를 HH:MM:SS,mmm 형식으로 변환합니다."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_float = seconds % 60
    seconds = int(seconds_float)
    milliseconds = int((seconds_float - seconds) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def parse_time(time_str):
    """HH:MM:SS 형식의 문자열을 초로 변환합니다."""
    try:
        hours, minutes, seconds = map(int, time_str.split(':'))
        return hours * 3600 + minutes * 60 + seconds
    except ValueError:
        return None 