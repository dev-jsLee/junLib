"""
XML 파일 처리를 위한 핸들러 클래스
"""
import os
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, List
from file_utils import path_exist
from xml_utils import (
    prettify_xml, xml_to_dict, search_xml_by_attribute,
    add_sub_element, remove_empty_tags, get_tag_content,
    get_tag_contents, xml_to_json, json_to_xml
)

class XMLHandler:
    """XML 파일 처리를 위한 핸들러 클래스"""
    
    def __init__(self, file_path: Optional[str] = None) -> None:
        """
        XMLHandler 초기화
        
        Args:
            file_path (str, optional): XML 파일 경로
        """
        self.file_path = file_path
        self.tree = None
        self.root = None
        if file_path:
            self.load(file_path)
    
    def load(self, file_path: str) -> 'XMLHandler':
        """
        XML 파일을 로드합니다.
        
        Args:
            file_path (str): 로드할 파일 경로
            
        Returns:
            XMLHandler: 체이닝을 위한 self 반환
            
        Raises:
            FileNotFoundError: 파일이 존재하지 않을 때
            ET.ParseError: XML 파싱 오류 발생 시
        """
        if not path_exist(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
            
        self.file_path = file_path
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()
        return self
    
    def save(self, file_path: Optional[str] = None, pretty: bool = True) -> 'XMLHandler':
        """
        XML 파일을 저장합니다.
        
        Args:
            file_path (str, optional): 저장할 파일 경로
            pretty (bool): 들여쓰기 적용 여부
            
        Returns:
            XMLHandler: 체이닝을 위한 self 반환
        """
        if file_path:
            self.file_path = file_path
            
        if self.tree:
            if pretty:
                xml_str = ET.tostring(self.root, encoding='utf-8').decode('utf-8')
                pretty_xml = prettify_xml(xml_str)
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    f.write(pretty_xml)
            else:
                self.tree.write(self.file_path, encoding='utf-8', xml_declaration=True)
        return self
    
    def get_root(self) -> ET.Element:
        """
        루트 요소를 반환합니다.
        
        Returns:
            ET.Element: 루트 요소
        """
        return self.root
    
    def get_tree(self) -> ET.ElementTree:
        """
        ElementTree 객체를 반환합니다.
        
        Returns:
            ET.ElementTree: ElementTree 객체
        """
        return self.tree
    
    def to_dict(self) -> Dict[str, Any]:
        """
        XML을 딕셔너리로 변환합니다.
        
        Returns:
            Dict[str, Any]: 변환된 딕셔너리
        """
        return xml_to_dict(self.root)
    
    def find_tag(self, tag_name: str) -> Optional[ET.Element]:
        """
        특정 태그를 찾습니다.
        
        Args:
            tag_name (str): 찾을 태그명
            
        Returns:
            Optional[ET.Element]: 찾은 태그 (없으면 None)
        """
        return self.root.find(f'.//{tag_name}')
    
    def find_all_tags(self, tag_name: str) -> List[ET.Element]:
        """
        특정 태그를 모두 찾습니다.
        
        Args:
            tag_name (str): 찾을 태그명
            
        Returns:
            List[ET.Element]: 찾은 태그 목록
        """
        return self.root.findall(f'.//{tag_name}')
    
    def get_tag_content(self, tag_name: str) -> Optional[str]:
        """
        특정 태그의 내용을 가져옵니다.
        
        Args:
            tag_name (str): 찾을 태그명
            
        Returns:
            Optional[str]: 태그의 내용 (없으면 None)
        """
        return get_tag_content(self.root, tag_name)
    
    def get_tag_contents(self, tag_name: str) -> List[str]:
        """
        특정 태그의 모든 내용을 가져옵니다.
        
        Args:
            tag_name (str): 찾을 태그명
            
        Returns:
            List[str]: 태그의 내용 목록
        """
        return get_tag_contents(self.root, tag_name)
    
    def add_sub(self, parent: ET.Element, child_name: str, text: str = '') -> ET.Element:
        """
        부모 요소에 자식 요소를 추가합니다.
        
        Args:
            parent (ET.Element): 부모 요소
            child_name (str): 추가할 자식 요소의 이름
            text (str, optional): 자식 요소의 텍스트
            
        Returns:
            ET.Element: 추가된 자식 요소
        """
        return add_sub_element(parent, child_name, text)
    
    def remove_empty_tags(self) -> 'XMLHandler':
        """
        빈 태그를 제거합니다.
        
        Returns:
            XMLHandler: 체이닝을 위한 self 반환
        """
        remove_empty_tags(self.root)
        return self
    
    def search_by_attribute(self, tag_name: str, attribute_name: str, attribute_value: str) -> List[tuple]:
        """
        속성값으로 태그를 검색합니다.
        
        Args:
            tag_name (str): 검색할 태그명
            attribute_name (str): 검색할 속성명
            attribute_value (str): 검색할 속성값
            
        Returns:
            List[tuple]: 일치하는 태그의 정보 (태그명, 속성들)
        """
        return search_xml_by_attribute(self.file_path, tag_name, attribute_name, attribute_value)
    
    def to_json(self) -> Dict[str, Any]:
        """
        XML을 JSON 형식의 딕셔너리로 변환합니다.
        
        Returns:
            Dict[str, Any]: 변환된 JSON 형식의 딕셔너리
        """
        return xml_to_json(self.root)
    
    def from_json(self, json_data: Dict[str, Any], root_name: str = 'root') -> 'XMLHandler':
        """
        JSON 데이터로부터 XML을 생성합니다.
        
        Args:
            json_data (Dict[str, Any]): JSON 데이터
            root_name (str): 루트 요소의 이름
            
        Returns:
            XMLHandler: 체이닝을 위한 self 반환
        """
        self.root = json_to_xml(json_data, root_name)
        self.tree = ET.ElementTree(self.root)
        return self

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
        
        # 테스트 파일 생성
        with open("test.xml", "w", encoding="utf-8") as f:
            f.write(test_xml)
        
        # XML 핸들러 테스트
        handler = XMLHandler("test.xml")
        
        # 태그 내용 가져오기
        name = handler.get_tag_content("name")
        print("이름:", name)
        
        # 모든 이름 가져오기
        names = handler.get_tag_contents("name")
        print("모든 이름:", names)
        
        # 딕셔너리로 변환
        data = handler.to_dict()
        print("딕셔너리:", data)
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
    finally:
        # 테스트 파일 삭제
        if path_exist("test.xml"):
            os.remove("test.xml")
            print("테스트 파일이 삭제되었습니다.") 