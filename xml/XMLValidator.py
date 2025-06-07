"""
XML 파일 검증을 위한 클래스들
"""
import xml
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os
import sys
from .. import junLib

class XMLController:
    def __init__(self, xml_file=None):
        self.xml_file = xml_file
        self.parse()
            
    def parse(self):
        if self.xml_file:
            self.tree = ET.parse(self.xml_file)
            self.root = self.tree.getroot()
        else:
            print('self.xml_file is None.')
        
    def save(self):
        self.tree = ET.ElementTree(self.root)
        self.tree.write(self.xml_file, encoding='utf-8',xml_declaration=True)
        self.prettify_xml()
        return self.xml_file

    def prettify_xml(self, input_file=None, output_file=None):
        if not input_file:
            input_file = self.xml_file
            pass
        # XML 파일을 minidom으로 파싱
        dom = minidom.parse(input_file)
        if not output_file:
            output_file = input_file

        # XML을 들여쓰기 형식으로 변환한 후, 빈 줄을 제거
        xml_str = dom.toprettyxml(indent="    ")
        xml_lines = xml_str.splitlines()
        non_empty_lines = [line for line in xml_lines if line.strip()]
        result = "\n".join(non_empty_lines)

        # 정제된 XML을 파일로 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)

    def replace_specific_tags(self, parent_tag, target_tag, new_content):
        parent_elems = self.root.findall('.//' + parent_tag)
        for parent_elem in parent_elems:
            target_elems = parent_elem.findall(target_tag)
            for target_elem in target_elems:
                target_elem.text = new_content
        self.save()
        return self

    def insert_text_into_tag(self, insert_tag: str, insert_text: str, target_tag_str: str=None, target_tag_ele: ET.Element=None, root: os.path=None):
        # if not self.root:
            # self.root = root
        target_elems = None
        insert_elem = None
        if target_tag_str:
            target_elems = self.root.findall('.//' + target_tag_str)
            for target_elem in target_elems:
                insert_elem = ET.Element(insert_tag)
                insert_elem.text = insert_text
                target_elem.insert(0, insert_elem)
        elif target_tag_ele:
            target_elem = target_tag_ele
            insert_elem = ET.Element(insert_tag)
            insert_elem.text = insert_text
            target_elem.insert(0, insert_elem)
        self.save()
        return insert_elem

    def replace_tag_content(self, target_tag: str, new_content: str):
        target_elems = self.root.findall('.//' + target_tag)
        for target_elem in target_elems:
            target_elem.text = new_content
        self.save()
        return self

    def replace_tag_first_content(self, target_tag, new_content):
        target_elem = self.root.find('.//' + target_tag)
        target_elem.text = new_content
        self.save()
        return target_elem

    def get_tag_content(self, target_tag):
        target_elem = self.root.findall(f'.//{target_tag}')[0]
        if target_elem is not None:
            return target_elem.text
        return None

    def get_tags_content_list(self, target_tag):
        target_elems = self.root.findall(f'.//{target_tag}')
        if target_elems:
            result = []
            for i, target_elem in enumerate(target_elems):
                if target_elem is not None:
                    result.append(target_elem.text)
            return result
        else:
            return None

    def get_tags_content(self, target_tag):
        target_elems = self.root.findall(f'.//{target_tag}')
        if target_elems:
            target_elem = target_elems[0]
            result = []
            if target_elem is not None:
                result.append(target_elem.text)
            return result
        else:
            return None

    def remove_tag(self, target_tag):
        parent = None
        for elem in self.root.iter():
            if elem is not None:
                child = elem.find(target_tag)
                if child is not None:
                    parent = elem
                    parent.remove(child)
        self.save()
        return self

    def find_tag(self, target_tag):
        for elem in self.root.iter(target_tag):
            return elem
        return None

    def add_sub(self, parent_ele, child_str, text=''):
        child = ET.SubElement(parent_ele, child_str)
        if not text:
            child.text = text
        self.save()
        return child

    def xml_to_dict(self, element):
        result = {}
        if len(element) == 0:
            result[element.tag] = element.text
        else:
            result[element.tag] = {}
            for child in element:
                child_dict = self.xml_to_dict(child)
                if child.tag in result[element.tag]:
                    if isinstance(result[element.tag][child.tag], list):
                        result[element.tag][child.tag].append(child_dict)
                    else:
                        result[element.tag][child.tag] = [result[element.tag][child.tag], child_dict]
                else:
                    result[element.tag][child.tag] = child_dict
        return result

    def remove_empty_tags(self, xml_file_path=''):
        # XML 파일을 파싱하여 ElementTree 객체 생성
        tree = self.tree
        root = tree.getroot()

        # 빈 태그를 찾아서 삭제
        def remove_empty_elements(element):
            for child in list(element):
                remove_empty_elements(child)

            if not element.text and not element.attrib and not list(element):
                self.remove_tag(element.tag)

        remove_empty_elements(root)

        # 수정된 XML 파일로 저장
        if xml_file_path:
            tree.write(xml_file_path, encoding="utf-8")
        else:
            tree.write(self.xml_file, encoding='utf-8')
    
    def search_xml_by_attribute(self, tag_name, attribute_name, attribute_value, xml_path=None):
        """
        XML 파일에서 주어진 태그와 속성값을 기반으로 태그를 검색하고 해당 태그의 정보를 반환합니다.

        :param xml_path: XML 파일의 경로
        :param tag_name: 검색하고자 하는 태그명
        :param attribute_name: 검색하고자 하는 속성명
        :param attribute_value: 검색하고자 하는 속성값
        :return: 일치하는 태그의 정보 (태그명, 속성들)
        """
        tree = self.tree
        if xml_path:
            tree = ET.parse(xml_path)
        root = tree.getroot()

        results = []

        for elem in root.iter(tag_name):
            if elem.attrib.get(attribute_name) == attribute_value:
                results.append((elem.tag, elem.attrib))

        return results
    
class XMLMaker:
    def __init__(self, root_tag_name, file_path=None) -> None:
        self.root = ET.Element(root_tag_name, {'xmlns:xs':"http://www.w3.org/2001/XMLSchema"})
        self.tree = ET.ElementTree(self.root)
        if file_path:
            self.set_file_path(file_path)

    def set_file_path(self, file_path):
        self.file_path = file_path
        self.save()
        return self

    def save(self):
        if self.file_path:
            self.tree.write(self.file_path, encoding='utf-8')
        else:
            print('Not Exist file_path. Plz use "set_file_path(file_path)" to set file path before save()')
        return self
    
    def use_xml_controller(self):
        if not self.controller:
            self.controller = XMLController(self.file_path)
        return self.controller