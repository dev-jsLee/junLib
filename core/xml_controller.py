"""
XML 파일 처리를 위한 컨트롤러 클래스
"""
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os
from typing import Dict, Any, List, Optional, Tuple

class XMLController:
    """XML 파일 처리를 위한 컨트롤러 클래스"""
    
    def __init__(self, xml_file: Optional[str] = None) -> None:
        """
        XMLController 초기화
        
        Args:
            xml_file (str, optional): XML 파일 경로
        """
        self.xml_file = xml_file
        self.tree = None
        self.root = None
        if xml_file:
            self.parse()
    
    def parse(self) -> 'XMLController':
        """
        XML 파일을 파싱합니다.
        
        Returns:
            XMLController: 체이닝을 위한 self 반환
            
        Raises:
            FileNotFoundError: 파일이 존재하지 않을 때
            ET.ParseError: XML 파싱 오류 발생 시
        """
        if not self.xml_file:
            raise ValueError("XML 파일 경로가 설정되지 않았습니다.")
            
        if not os.path.exists(self.xml_file):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {self.xml_file}")
            
        self.tree = ET.parse(self.xml_file)
        self.root = self.tree.getroot()
        return self
    
    def save(self, pretty: bool = True) -> 'XMLController':
        """
        XML 파일을 저장합니다.
        
        Args:
            pretty (bool): 들여쓰기 적용 여부
            
        Returns:
            XMLController: 체이닝을 위한 self 반환
        """
        if not self.tree:
            raise ValueError("저장할 XML 데이터가 없습니다.")
            
        if pretty:
            xml_str = ET.tostring(self.root, encoding='utf-8').decode('utf-8')
            dom = minidom.parseString(xml_str)
            pretty_xml = dom.toprettyxml(indent="    ")
            with open(self.xml_file, 'w', encoding='utf-8') as f:
                f.write(pretty_xml)
        else:
            self.tree.write(self.xml_file, encoding='utf-8', xml_declaration=True)
        return self
    
    def validate_xml(self) -> bool:
        """
        XML 파일의 유효성을 검사합니다.
        
        Returns:
            bool: 유효성 검사 결과
        """
        try:
            ET.parse(self.xml_file)
            return True
        except ET.ParseError:
            return False
    
    def validate_against_schema(self, schema_file: str) -> bool:
        """
        XML 파일이 XSD 스키마를 준수하는지 검사합니다.
        
        Args:
            schema_file (str): XSD 스키마 파일 경로
            
        Returns:
            bool: 스키마 검증 결과
        """
        try:
            import lxml.etree as etree
            schema = etree.XMLSchema(file=schema_file)
            xml = etree.parse(self.xml_file)
            return schema.validate(xml)
        except Exception:
            return False
    
    def get_tag_content(self, target_tag: str) -> Optional[str]:
        """
        특정 태그의 내용을 가져옵니다.
        
        Args:
            target_tag (str): 찾을 태그명
            
        Returns:
            Optional[str]: 태그의 내용 (없으면 None)
        """
        target_elem = self.root.find(f'.//{target_tag}')
        return target_elem.text if target_elem is not None else None
    
    def get_tag_contents(self, target_tag: str) -> List[str]:
        """
        특정 태그의 모든 내용을 가져옵니다.
        
        Args:
            target_tag (str): 찾을 태그명
            
        Returns:
            List[str]: 태그의 내용 목록
        """
        target_elems = self.root.findall(f'.//{target_tag}')
        return [elem.text for elem in target_elems if elem.text]
    
    def replace_tag_content(self, target_tag: str, new_content: str) -> 'XMLController':
        """
        특정 태그의 내용을 변경합니다.
        
        Args:
            target_tag (str): 변경할 태그명
            new_content (str): 새로운 내용
            
        Returns:
            XMLController: 체이닝을 위한 self 반환
        """
        target_elems = self.root.findall(f'.//{target_tag}')
        for target_elem in target_elems:
            target_elem.text = new_content
        return self
    
    def add_sub_element(self, parent: ET.Element, child_name: str, text: str = '') -> ET.Element:
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
    
    def remove_tag(self, target_tag: str) -> 'XMLController':
        """
        특정 태그를 제거합니다.
        
        Args:
            target_tag (str): 제거할 태그명
            
        Returns:
            XMLController: 체이닝을 위한 self 반환
        """
        for elem in self.root.iter():
            if elem is not None:
                child = elem.find(target_tag)
                if child is not None:
                    elem.remove(child)
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """
        XML을 딕셔너리로 변환합니다.
        
        Returns:
            Dict[str, Any]: 변환된 딕셔너리
        """
        result = {}
        
        if len(self.root) == 0:
            result[self.root.tag] = self.root.text
        else:
            result[self.root.tag] = {}
            for child in self.root:
                child_dict = self._element_to_dict(child)
                if child.tag in result[self.root.tag]:
                    if isinstance(result[self.root.tag][child.tag], list):
                        result[self.root.tag][child.tag].append(child_dict)
                    else:
                        result[self.root.tag][child.tag] = [result[self.root.tag][child.tag], child_dict]
                else:
                    result[self.root.tag][child.tag] = child_dict
        return result
    
    def _element_to_dict(self, element: ET.Element) -> Dict[str, Any]:
        """
        XML 요소를 딕셔너리로 변환하는 내부 메서드
        
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
                child_dict = self._element_to_dict(child)
                if child.tag in result[element.tag]:
                    if isinstance(result[element.tag][child.tag], list):
                        result[element.tag][child.tag].append(child_dict)
                    else:
                        result[element.tag][child.tag] = [result[element.tag][child.tag], child_dict]
                else:
                    result[element.tag][child.tag] = child_dict
        return result

if __name__ == "__main__":
    # 테스트 코드
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
        
        # XML 컨트롤러 테스트
        controller = XMLController("test.xml")
        
        # 태그 내용 가져오기
        name = controller.get_tag_content("name")
        print("이름:", name)
        
        # 모든 이름 가져오기
        names = controller.get_tag_contents("name")
        print("모든 이름:", names)
        
        # 딕셔너리로 변환
        data = controller.to_dict()
        print("딕셔너리:", data)
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
    finally:
        # 테스트 파일 삭제
        if os.path.exists("test.xml"):
            os.remove("test.xml")
            print("테스트 파일이 삭제되었습니다.")