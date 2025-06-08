"""
JSON 파일 처리를 위한 유틸리티 함수들
"""
import os
import json
from typing import Dict, Any, Optional, Union

def is_valid_json(json_str: str) -> bool:
    """
    문자열이 유효한 JSON 형식인지 확인합니다.
    
    Args:
        json_str (str): 검사할 JSON 문자열
        
    Returns:
        bool: 유효한 JSON이면 True, 아니면 False
    """
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False

def file_exists(file_path: str) -> bool:
    """
    파일이 존재하는지 확인합니다.
    
    Args:
        file_path (str): 확인할 파일 경로
        
    Returns:
        bool: 파일이 존재하면 True, 아니면 False
    """
    return os.path.isfile(file_path)

def write_to_json(json_data: Dict[str, Any], json_file_path: str, formatting: bool = True, sort: bool = False) -> None:
    """
    JSON 데이터를 파일로 저장합니다.
    
    Args:
        json_data (Dict[str, Any]): 저장할 JSON 데이터
        json_file_path (str): 저장할 파일 경로
        formatting (bool): 들여쓰기 적용 여부
        sort (bool): 키 정렬 여부
        
    Raises:
        ValueError: json_data가 유효한 JSON 형식이 아닐 때
    """
    if not isinstance(json_data, dict):
        raise ValueError("json_data는 딕셔너리여야 합니다.")
        
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(
            obj=json_data, 
            fp=json_file, 
            indent=(4 if formatting else None),
            sort_keys=sort,
            ensure_ascii=False
        )

def read_from_json(json_file_path: str) -> Dict[str, Any]:
    """
    JSON 파일을 읽어서 데이터를 반환합니다.
    
    Args:
        json_file_path (str): 읽을 JSON 파일 경로
        
    Returns:
        Dict[str, Any]: JSON 데이터
        
    Raises:
        FileNotFoundError: 파일이 존재하지 않을 때
        json.JSONDecodeError: 파일이 유효한 JSON 형식이 아닐 때
    """
    if not file_exists(json_file_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {json_file_path}")
        
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def insert_to_dict(target_dict: Dict[str, Any], new_key: str, new_value: Any, index: int = -1) -> Dict[str, Any]:
    """
    딕셔너리에 새로운 키-값 쌍을 특정 위치에 삽입합니다.
    
    Args:
        target_dict (Dict[str, Any]): 대상 딕셔너리
        new_key (str): 삽입할 키
        new_value (Any): 삽입할 값
        index (int): 삽입할 위치 (-1이면 마지막에 삽입)
        
    Returns:
        Dict[str, Any]: 수정된 딕셔너리
    """
    if not isinstance(target_dict, dict):
        raise ValueError("target_dict는 딕셔너리여야 합니다.")
        
    if index == -1:
        index = len(target_dict) - 1
    
    new_dict = {}
    for i, (key, value) in enumerate(target_dict.items()):
        if i == index:
            new_dict[new_key] = new_value
        new_dict[key] = value
    return new_dict

def insert_after_key(target_dict: Dict[str, Any], new_key: str, new_value: Any, target_key: str) -> Dict[str, Any]:
    """
    딕셔너리에 새로운 키-값 쌍을 특정 키 다음에 삽입합니다.
    
    Args:
        target_dict (Dict[str, Any]): 대상 딕셔너리
        new_key (str): 삽입할 키
        new_value (Any): 삽입할 값
        target_key (str): 기준이 되는 키
        
    Returns:
        Dict[str, Any]: 수정된 딕셔너리
        
    Raises:
        KeyError: target_key가 딕셔너리에 없을 때
    """
    if not isinstance(target_dict, dict):
        raise ValueError("target_dict는 딕셔너리여야 합니다.")
        
    if target_key not in target_dict:
        raise KeyError(f"키를 찾을 수 없습니다: {target_key}")
        
    new_dict = {}
    for key, value in target_dict.items():
        new_dict[key] = value
        if key == target_key:
            new_dict[new_key] = new_value
    return new_dict

def insert_before_key(target_dict: Dict[str, Any], new_key: str, new_value: Any, target_key: str) -> Dict[str, Any]:
    """
    딕셔너리에 새로운 키-값 쌍을 특정 키 이전에 삽입합니다.
    
    Args:
        target_dict (Dict[str, Any]): 대상 딕셔너리
        new_key (str): 삽입할 키
        new_value (Any): 삽입할 값
        target_key (str): 기준이 되는 키
        
    Returns:
        Dict[str, Any]: 수정된 딕셔너리
        
    Raises:
        KeyError: target_key가 딕셔너리에 없을 때
    """
    if not isinstance(target_dict, dict):
        raise ValueError("target_dict는 딕셔너리여야 합니다.")
        
    if target_key not in target_dict:
        raise KeyError(f"키를 찾을 수 없습니다: {target_key}")
        
    new_dict = {}
    for key, value in target_dict.items():
        if key == target_key:
            new_dict[new_key] = new_value
        new_dict[key] = value
    return new_dict

if __name__ == "__main__":
    # 테스트용 JSON 데이터
    test_data = {
        "name": "John",
        "age": 30,
        "city": "New York"
    }
    
    try:
        # 파일 저장 테스트
        write_to_json(test_data, "test.json", formatting=True)
        print("JSON 파일이 생성되었습니다.")
        
        # 파일 읽기 테스트
        loaded_data = read_from_json("test.json")
        print("읽은 데이터:", loaded_data)
        
        # 딕셔너리 수정 테스트
        modified_data = insert_to_dict(test_data, "country", "USA", 1)
        print("수정된 데이터:", modified_data)
        
        # 키 기준 삽입 테스트
        after_data = insert_after_key(test_data, "country", "USA", "age")
        print("age 키 이후 삽입:", after_data)
        
        before_data = insert_before_key(test_data, "country", "USA", "age")
        print("age 키 이전 삽입:", before_data)
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
    finally:
        # 테스트 파일 삭제
        if file_exists("test.json"):
            os.remove("test.json")
            print("테스트 파일이 삭제되었습니다.") 