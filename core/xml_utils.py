"""
XML 파일 처리를 위한 유틸리티 함수들
"""
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from typing import Dict, Any, List, Optional, Tuple
from file_utils import path_exist

def prettify_xml(xml_string: str) -> str:
    """
    XML 문자열을 보기 좋게 포맷팅합니다.
    
    Args:
        xml_string (str): 포맷팅할 XML 문자열
        
    Returns:
        str: 포맷팅된 XML 문자열
    """
    dom = minidom.parseString(xml_string)
    return dom.toprettyxml(indent="    ")

def xml_to_dict(element: ET.Element) -> Dict[str, Any]:
    """
    XML 요소를 딕셔너리로 변환합니다.
    
    Args:
        element (ET.Element): 변환할 XML 요소
        
    Returns:
        Dict[str, Any]: 변환된 딕셔너리
    """
    result = {}
    
    if len(element) == 0:
        result[element.tag] = element.text
    else:
        result[element.tag] = {}
        for child in element:
            child_dict = xml_to_dict(child)
            if child.tag in result[element.tag]:
                if isinstance(result[element.tag][child.tag], list):
                    result[element.tag][child.tag].append(child_dict)
                else:
                    result[element.tag][child.tag] = [result[element.tag][child.tag], child_dict]
            else:
                result[element.tag][child.tag] = child_dict
    return result

def search_xml_by_attribute(xml_path: str, tag_name: str, attribute_name: str, attribute_value: str) -> List[Tuple[str, Dict[str, str]]]:
    """
    XML 파일에서 주어진 태그와 속성값을 기반으로 태그를 검색합니다.
    
    Args:
        xml_path (str): XML 파일 경로
        tag_name (str): 검색할 태그명
        attribute_name (str): 검색할 속성명
        attribute_value (str): 검색할 속성값
        
    Returns:
        List[Tuple[str, Dict[str, str]]]: 일치하는 태그의 정보 (태그명, 속성들)
    """
    if not path_exist(xml_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {xml_path}")
        
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    results = []
    for elem in root.iter(tag_name):
        if elem.attrib.get(attribute_name) == attribute_value:
            results.append((elem.tag, elem.attrib))
            
    return results

def add_sub_element(parent: ET.Element, child_name: str, text: str = '') -> ET.Element:
    """
    부모 요소에 자식 요소를 추가합니다.
    
    Args:
        parent (ET.Element): 부모 요소
        child_name (str): 추가할 자식 요소의 이름
        text (str, optional): 자식 요소의 텍스트
        
    Returns:
        ET.Element: 추가된 자식 요소
    """
    child = ET.SubElement(parent, child_name)
    if text:
        child.text = text
    return child

def remove_empty_tags(element: ET.Element) -> None:
    """
    XML 요소에서 빈 태그를 제거합니다.
    
    Args:
        element (ET.Element): 처리할 XML 요소
    """
    for child in list(element):
        remove_empty_tags(child)
        
    if not element.text and not element.attrib and not list(element):
        parent = element.getparent()
        if parent is not None:
            parent.remove(element)

def get_tag_content(element: ET.Element, target_tag: str) -> Optional[str]:
    """
    특정 태그의 내용을 가져옵니다.
    
    Args:
        element (ET.Element): 검색할 XML 요소
        target_tag (str): 찾을 태그명
        
    Returns:
        Optional[str]: 태그의 내용 (없으면 None)
    """
    target_elem = element.find(f'.//{target_tag}')
    return target_elem.text if target_elem is not None else None

def get_tag_contents(element: ET.Element, target_tag: str) -> List[str]:
    """
    특정 태그의 모든 내용을 가져옵니다.
    
    Args:
        element (ET.Element): 검색할 XML 요소
        target_tag (str): 찾을 태그명
        
    Returns:
        List[str]: 태그의 내용 목록
    """
    target_elems = element.findall(f'.//{target_tag}')
    return [elem.text for elem in target_elems if elem.text]

def xml_to_json(element: ET.Element) -> Dict[str, Any]:
    """
    XML 요소를 JSON 형식의 딕셔너리로 변환합니다.
    
    Args:
        element (ET.Element): 변환할 XML 요소
        
    Returns:
        Dict[str, Any]: 변환된 JSON 형식의 딕셔너리
    """
    json_data = {}
    
    # 태그의 텍스트 값이 있으면 __text__ 키로 저장
    if element.text and element.text.strip():
        json_data['__text__'] = element.text.strip()
    
    # 태그의 속성이 있으면 해당 속성을 저장
    for key, value in element.attrib.items():
        json_data[key] = value
    
    # 자식 태그가 있으면 재귀적으로 호출하여 저장
    for child in element:
        child_data = xml_to_json(child)
        if child.tag not in json_data:
            json_data[child.tag] = child_data
        else:
            if not isinstance(json_data[child.tag], list):
                json_data[child.tag] = [json_data[child.tag]]
            json_data[child.tag].append(child_data)
    
    return json_data

def json_to_xml(json_data: Dict[str, Any], root_name: str = 'root') -> ET.Element:
    """
    JSON 형식의 딕셔너리를 XML 요소로 변환합니다.
    
    Args:
        json_data (Dict[str, Any]): 변환할 JSON 데이터
        root_name (str): 루트 요소의 이름
        
    Returns:
        ET.Element: 변환된 XML 요소
    """
    root = ET.Element(root_name)
    _add_json_to_xml(root, json_data)
    return root

def _add_json_to_xml(parent_element: ET.Element, data: Dict[str, Any]) -> None:
    """
    JSON 데이터를 XML 요소에 추가하는 내부 함수
    
    Args:
        parent_element (ET.Element): 부모 XML 요소
        data (Dict[str, Any]): 추가할 JSON 데이터
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if key == '__text__':
                parent_element.text = str(value)
            elif isinstance(value, list):
                for item in value:
                    child = ET.Element(key)
                    _add_json_to_xml(child, item)
                    parent_element.append(child)
            elif isinstance(value, dict):
                child = ET.Element(key)
                _add_json_to_xml(child, value)
                parent_element.append(child)
            else:
                parent_element.set(key, str(value))
    elif isinstance(data, list):
        for item in data:
            child = ET.Element(parent_element.tag)
            _add_json_to_xml(child, item)
            parent_element.append(child)
    else:
        parent_element.text = str(data)

if __name__ == "__main__":
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
    
    try:
        # XML 파싱 테스트
        root = ET.fromstring(test_xml)
        
        # 태그 내용 가져오기 테스트
        name = get_tag_content(root, "name")
        print("이름:", name)
        
        # 모든 이름 가져오기 테스트
        names = get_tag_contents(root, "name")
        print("모든 이름:", names)
        
        # 속성으로 검색 테스트
        results = search_xml_by_attribute("test.xml", "person", "id", "1")
        print("검색 결과:", results)
        
    except Exception as e:
        print(f"오류 발생: {str(e)}") 