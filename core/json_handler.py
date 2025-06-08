"""
JSON 파일 처리를 위한 핸들러 클래스
"""
import os
import json
from typing import Dict, Any, Optional
from json_utils import (
    write_to_json, read_from_json, insert_to_dict,
    insert_after_key, insert_before_key, file_exists,
    is_valid_json
)

class JSONController:
    """JSON 파일을 처리하기 위한 컨트롤러 클래스"""
    
    def __init__(self, json_data: Optional[Dict[str, Any]] = None, json_file_path: Optional[str] = None) -> None:
        """
        JSONController 초기화
        
        Args:
            json_data (Dict[str, Any], optional): JSON 데이터
            json_file_path (str, optional): JSON 파일 경로
        """
        self.json_data = json_data or {}
        self.json_file_path = json_file_path
    
    def get_data(self) -> Dict[str, Any]:
        """
        현재 JSON 데이터를 반환합니다.
        
        Returns:
            Dict[str, Any]: 현재 JSON 데이터
        """
        return self.json_data
    
    def set_json_data(self, json_data: Dict[str, Any]) -> 'JSONController':
        """
        JSON 데이터를 설정합니다.
        
        Args:
            json_data (Dict[str, Any]): 설정할 JSON 데이터
            
        Returns:
            JSONController: 체이닝을 위한 self 반환
            
        Raises:
            ValueError: json_data가 유효한 JSON 형식이 아닐 때
        """
        if not isinstance(json_data, dict):
            raise ValueError("json_data는 딕셔너리여야 합니다.")
        self.json_data = json_data
        return self
    
    def set_json_file_path(self, json_file_path: str) -> 'JSONController':
        """
        JSON 파일 경로를 설정합니다.
        
        Args:
            json_file_path (str): 설정할 파일 경로
            
        Returns:
            JSONController: 체이닝을 위한 self 반환
        """
        self.json_file_path = json_file_path
        return self
    
    def load(self, json_file_path: Optional[str] = None) -> 'JSONController':
        """
        JSON 파일을 로드합니다.
        
        Args:
            json_file_path (str, optional): 로드할 파일 경로
            
        Returns:
            JSONController: 체이닝을 위한 self 반환
            
        Raises:
            FileNotFoundError: 파일이 존재하지 않을 때
            json.JSONDecodeError: 파일이 유효한 JSON 형식이 아닐 때
        """
        if json_file_path:
            self.json_file_path = json_file_path
        if self.json_file_path:
            self.json_data = read_from_json(self.json_file_path)
        return self
    
    def save(self, json_file_path: Optional[str] = None, formatting: bool = True, sort: bool = False) -> 'JSONController':
        """
        JSON 데이터를 파일로 저장합니다.
        
        Args:
            json_file_path (str, optional): 저장할 파일 경로
            formatting (bool): 들여쓰기 적용 여부
            sort (bool): 키 정렬 여부
            
        Returns:
            JSONController: 체이닝을 위한 self 반환
            
        Raises:
            ValueError: json_data가 유효한 JSON 형식이 아닐 때
        """
        if json_file_path:
            self.json_file_path = json_file_path
        if self.json_file_path:
            write_to_json(self.json_data, self.json_file_path, formatting, sort)
        return self
    
    def insert(self, new_key: str, new_value: Any, index: int = -1) -> 'JSONController':
        """
        JSON 데이터에 새로운 키-값 쌍을 특정 위치에 삽입합니다.
        
        Args:
            new_key (str): 삽입할 키
            new_value (Any): 삽입할 값
            index (int): 삽입할 위치 (-1이면 마지막에 삽입)
            
        Returns:
            JSONController: 체이닝을 위한 self 반환
        """
        self.json_data = insert_to_dict(self.json_data, new_key, new_value, index)
        return self
    
    def insert_after(self, new_key: str, new_value: Any, target_key: str) -> 'JSONController':
        """
        JSON 데이터에 새로운 키-값 쌍을 특정 키 다음에 삽입합니다.
        
        Args:
            new_key (str): 삽입할 키
            new_value (Any): 삽입할 값
            target_key (str): 기준이 되는 키
            
        Returns:
            JSONController: 체이닝을 위한 self 반환
            
        Raises:
            KeyError: target_key가 딕셔너리에 없을 때
        """
        self.json_data = insert_after_key(self.json_data, new_key, new_value, target_key)
        return self
    
    def insert_before(self, new_key: str, new_value: Any, target_key: str) -> 'JSONController':
        """
        JSON 데이터에 새로운 키-값 쌍을 특정 키 이전에 삽입합니다.
        
        Args:
            new_key (str): 삽입할 키
            new_value (Any): 삽입할 값
            target_key (str): 기준이 되는 키
            
        Returns:
            JSONController: 체이닝을 위한 self 반환
            
        Raises:
            KeyError: target_key가 딕셔너리에 없을 때
        """
        self.json_data = insert_before_key(self.json_data, new_key, new_value, target_key)
        return self

if __name__ == "__main__":
    try:
        # 테스트용 JSON 데이터
        test_data = {
            "name": "John",
            "age": 30,
            "city": "New York"
        }
        
        # 컨트롤러 인스턴스 생성
        controller = JSONController(test_data)
        
        # 체이닝을 사용한 데이터 수정
        controller.insert("country", "USA", 1) \
                  .insert_after("email", "john@example.com", "age") \
                  .insert_before("phone", "123-456-7890", "email")
        
        # 파일로 저장
        controller.save("test.json", formatting=True)
        print("JSON 파일이 생성되었습니다.")
        
        # 파일에서 로드
        new_controller = JSONController()
        new_controller.load("test.json")
        print("로드된 데이터:", new_controller.get_data())
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
    finally:
        # 테스트 파일 삭제
        if file_exists("test.json"):
            os.remove("test.json")
            print("테스트 파일이 삭제되었습니다.") 