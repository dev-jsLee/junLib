"""
XSD 파일 처리를 위한 유틸리티 함수들
"""
import os
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional
from file_utils import path_exist

def generate_xsd_element(xml_element: ET.Element) -> str:
    """
    XML 요소를 XSD 요소로 변환합니다.
    
    Args:
        xml_element (ET.Element): 변환할 XML 요소
        
    Returns:
        str: 생성된 XSD 문자열
    """
    if len(xml_element) > 0:
        xsd = f'<xs:complexType>\n<xs:sequence>\n'
        for child in xml_element:
            xsd += f'<xs:element name="{child.tag}"'
            for attr_key, attr_value in child.attrib.items():
                xsd += f' {attr_key}="{attr_value}"'
            xsd += ">\n"
            xsd += generate_xsd_element(child)
            xsd += f'</xs:element>\n'
        xsd += "</xs:sequence>\n</xs:complexType>\n"
    else:
        xsd = '<xs:simpleType>\n<xs:restriction base="xs:string" />\n</xs:simpleType>\n'
    return xsd

def generate_xsd_from_xml_file(xml_file_path: str) -> Optional[str]:
    """
    XML 파일로부터 XSD를 생성합니다.
    
    Args:
        xml_file_path (str): XML 파일 경로
        
    Returns:
        Optional[str]: 생성된 XSD 문자열 (실패 시 None)
    """
    try:
        if not path_exist(xml_file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {xml_file_path}")
            
        # XML 파일 읽기
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # XSD 생성
        xsd = f'<xs:element name="{root.tag}">\n'
        xsd += generate_xsd_element(root)
        xsd += "</xs:element>"

        return xsd
    except Exception as e:
        print(f"XSD 생성 중 오류 발생: {str(e)}")
        return None

def generate_xsd_from_xml_string(xml_string: str) -> Optional[str]:
    """
    XML 문자열로부터 XSD를 생성합니다.
    
    Args:
        xml_string (str): XML 문자열
        
    Returns:
        Optional[str]: 생성된 XSD 문자열 (실패 시 None)
    """
    try:
        # XML 파싱
        root = ET.fromstring(xml_string)

        # XSD 생성
        xsd = f'<xs:element name="{root.tag}">\n'
        xsd += generate_xsd_element(root)
        xsd += "</xs:element>"

        return xsd
    except ET.ParseError as e:
        print(f"XML 파싱 중 오류 발생: {str(e)}")
        return None

def write_xsd_to_file(xsd_string: str, file_path: str) -> bool:
    """
    XSD 문자열을 파일로 저장합니다.
    
    Args:
        xsd_string (str): 저장할 XSD 문자열
        file_path (str): 저장할 파일 경로
        
    Returns:
        bool: 저장 성공 여부
    """
    try:
        # XSD 네임스페이스 선언 추가
        xsd_str = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">\n' + \
                 xsd_string + \
                 '</xs:schema>'
                 
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(xsd_str)
        return True
    except Exception as e:
        print(f"XSD 파일 저장 중 오류 발생: {str(e)}")
        return False

def generate_xsd_from_json(json_data: Dict[str, Any], root_name: str = 'root') -> str:
    """
    JSON 데이터로부터 XSD를 생성합니다.
    
    Args:
        json_data (Dict[str, Any]): JSON 데이터
        root_name (str): 루트 요소의 이름
        
    Returns:
        str: 생성된 XSD 문자열
    """
    xsd = f'<xs:element name="{root_name}">\n'
    xsd += _generate_xsd_from_json_data(json_data)
    xsd += "</xs:element>"
    return xsd

def _generate_xsd_from_json_data(data: Dict[str, Any]) -> str:
    """
    JSON 데이터를 XSD 요소로 변환하는 내부 함수
    
    Args:
        data (Dict[str, Any]): 변환할 JSON 데이터
        
    Returns:
        str: 생성된 XSD 문자열
    """
    if isinstance(data, dict):
        xsd = '<xs:complexType>\n<xs:sequence>\n'
        for key, value in data.items():
            if key == '__text__':
                continue
            xsd += f'<xs:element name="{key}"'
            if isinstance(value, list):
                xsd += ' maxOccurs="unbounded"'
                if len(value) > 0:
                    xsd += ">\n"
                    xsd += _generate_xsd_from_json_data(value[0])
                    xsd += "</xs:element>\n"
                else:
                    xsd += ' type="xs:string" />\n'
            elif isinstance(value, dict):
                xsd += ">\n"
                xsd += _generate_xsd_from_json_data(value)
                xsd += "</xs:element>\n"
            else:
                xsd += ' type="xs:string" />\n'
        xsd += "</xs:sequence>\n</xs:complexType>\n"
        return xsd
    else:
        return '<xs:simpleType>\n<xs:restriction base="xs:string" />\n</xs:simpleType>\n'

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
        xsd = generate_xsd_from_xml_string(test_xml)
        if xsd:
            print("생성된 XSD:")
            print(xsd)
            
            # XSD 파일로 저장
            if write_xsd_to_file(xsd, "test.xsd"):
                print("XSD 파일이 생성되었습니다.")
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
    finally:
        # 테스트 파일 삭제
        if path_exist("test.xsd"):
            os.remove("test.xsd")
            print("테스트 파일이 삭제되었습니다.") 