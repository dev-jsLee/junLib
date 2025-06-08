"""
XSD 파일 처리를 위한 핸들러 클래스
"""
import os
import xml.etree.ElementTree as ET
from typing import Optional, Dict, Any
from file_utils import path_exist
from xsd_utils import (
    generate_xsd_from_xml_file, generate_xsd_from_xml_string,
    write_xsd_to_file, generate_xsd_from_json
)

class XSDHandler:
    """
    XSD 파일 처리를 위한 핸들러 클래스
    """
    def __init__(self, xml_file_path: Optional[str] = None, xml_string: Optional[str] = None):
        """
        XSDHandler 초기화
        
        Args:
            xml_file_path (Optional[str]): XML 파일 경로
            xml_string (Optional[str]): XML 문자열
        """
        self.xml_file_path = xml_file_path
        self.xml_string = xml_string
        self.xsd_string = None
        
    def set_xml_file(self, file_path: str) -> 'XSDHandler':
        """
        XML 파일 경로를 설정합니다.
        
        Args:
            file_path (str): XML 파일 경로
            
        Returns:
            XSDHandler: 체이닝을 위한 self 반환
        """
        if not path_exist(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        self.xml_file_path = file_path
        self.xml_string = None
        return self
        
    def set_xml_string(self, xml_string: str) -> 'XSDHandler':
        """
        XML 문자열을 설정합니다.
        
        Args:
            xml_string (str): XML 문자열
            
        Returns:
            XSDHandler: 체이닝을 위한 self 반환
        """
        self.xml_string = xml_string
        self.xml_file_path = None
        return self
        
    def set_json_data(self, json_data: Dict[str, Any], root_name: str = 'root') -> 'XSDHandler':
        """
        JSON 데이터를 설정합니다.
        
        Args:
            json_data (Dict[str, Any]): JSON 데이터
            root_name (str): 루트 요소의 이름
            
        Returns:
            XSDHandler: 체이닝을 위한 self 반환
        """
        self.json_data = json_data
        self.root_name = root_name
        self.xml_file_path = None
        self.xml_string = None
        return self
        
    def generate(self) -> 'XSDHandler':
        """
        XSD를 생성합니다.
        
        Returns:
            XSDHandler: 체이닝을 위한 self 반환
            
        Raises:
            ValueError: XML 소스가 설정되지 않은 경우
        """
        if self.xml_file_path:
            self.xsd_string = generate_xsd_from_xml_file(self.xml_file_path)
        elif self.xml_string:
            self.xsd_string = generate_xsd_from_xml_string(self.xml_string)
        else:
            raise ValueError("XML 파일 경로 또는 XML 문자열이 설정되지 않았습니다.")
        return self
        
    def generate_from_json(self) -> 'XSDHandler':
        """
        JSON 데이터로부터 XSD를 생성합니다.
        
        Returns:
            XSDHandler: 체이닝을 위한 self 반환
            
        Raises:
            ValueError: JSON 데이터가 설정되지 않은 경우
        """
        if not hasattr(self, 'json_data'):
            raise ValueError("JSON 데이터가 설정되지 않았습니다.")
        self.xsd_string = generate_xsd_from_json(self.json_data, self.root_name)
        return self
        
    def save(self, file_path: str) -> bool:
        """
        XSD를 파일로 저장합니다.
        
        Args:
            file_path (str): 저장할 파일 경로
            
        Returns:
            bool: 저장 성공 여부
            
        Raises:
            ValueError: XSD가 생성되지 않은 경우
        """
        if not self.xsd_string:
            raise ValueError("XSD가 생성되지 않았습니다. generate() 메서드를 먼저 호출하세요.")
        return write_xsd_to_file(self.xsd_string, file_path)
        
    def get_xsd(self) -> Optional[str]:
        """
        생성된 XSD 문자열을 반환합니다.
        
        Returns:
            Optional[str]: XSD 문자열 (생성되지 않은 경우 None)
        """
        return self.xsd_string

if __name__ == "__main__":
    try:
        # 테스트용 XML 데이터
        test_xml = """
        <root>
            <person id="1">
                <name>홍길동</name>
                <age>30</age>
            </person>
            <person id="2">
                <name>김철수</name>
                <age>25</age>
            </person>
        </root>
        """
        
        # XML 문자열로부터 XSD 생성
        handler = XSDHandler(xml_string=test_xml)
        handler.generate()
        
        # 생성된 XSD 출력
        print("생성된 XSD:")
        print(handler.get_xsd())
        
        # XSD 파일로 저장
        if handler.save("test.xsd"):
            print("XSD 파일이 생성되었습니다.")
            
    except Exception as e:
        print(f"오류 발생: {str(e)}")
    finally:
        # 테스트 파일 삭제
        if path_exist("test.xsd"):
            os.remove("test.xsd")
            print("테스트 파일이 삭제되었습니다.") 