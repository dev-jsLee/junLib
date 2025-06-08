"""
피클 파일 처리를 위한 유틸리티 함수들
"""
import os
import pickle
from typing import Any, Optional
from file_utils import path_exist

def write_to_pkl(data: Any, pkl_file_path: str, protocol: Optional[int] = None) -> None:
    """
    데이터를 피클 파일로 저장합니다.
    
    Args:
        data (Any): 저장할 데이터
        pkl_file_path (str): 저장할 파일 경로
        protocol (int, optional): 피클 프로토콜 버전 (기본값: 최신 버전)
        
    Raises:
        ValueError: 데이터가 None일 때
        IOError: 파일 쓰기 실패 시
    """
    if data is None:
        raise ValueError("저장할 데이터가 None입니다.")
        
    try:
        with open(pkl_file_path, 'wb') as f:
            pickle.dump(data, f, protocol=protocol)
    except Exception as e:
        raise IOError(f"파일 저장 중 오류 발생: {str(e)}")

def load_pkl(pkl_file_path: str) -> Any:
    """
    피클 파일에서 데이터를 로드합니다.
    
    Args:
        pkl_file_path (str): 로드할 파일 경로
        
    Returns:
        Any: 로드된 데이터
        
    Raises:
        FileNotFoundError: 파일이 존재하지 않을 때
        IOError: 파일 읽기 실패 시
        pickle.UnpicklingError: 피클 데이터가 손상되었을 때
    """
    if not path_exist(pkl_file_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {pkl_file_path}")
        
    try:
        with open(pkl_file_path, 'rb') as f:
            return pickle.load(f)
    except pickle.UnpicklingError as e:
        raise pickle.UnpicklingError(f"피클 데이터가 손상되었습니다: {str(e)}")
    except Exception as e:
        raise IOError(f"파일 읽기 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    try:
        # 테스트용 데이터
        test_data = {
            "name": "홍길동",
            "age": 30,
            "scores": [90, 85, 95],
            "info": {"city": "서울", "job": "개발자"}
        }
        
        # 파일 저장 테스트
        write_to_pkl(test_data, "test.pkl")
        print("피클 파일이 생성되었습니다.")
        
        # 파일 읽기 테스트
        loaded_data = load_pkl("test.pkl")
        print("로드된 데이터:", loaded_data)
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
    finally:
        # 테스트 파일 삭제
        if path_exist("test.pkl"):
            os.remove("test.pkl")
            print("테스트 파일이 삭제되었습니다.")