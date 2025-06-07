# junLib_xml.py
import xml.etree.ElementTree as ET
import xml
import os
import sys
from __init__ import source_code_path
sys.path.append(source_code_path)
from _workplace.library.junLib import *
import codecs

def change_xml_encoding(input_file_path, output_file_path=None, new_encoding='utf-8'):
    # XML 파일을 원래의 인코딩으로 읽기
    with codecs.open(input_file_path, 'r') as f:
        content = f.read()
    
    output_file_path = output_file_path or input_file_path
    # 새로운 인코딩으로 XML 파일 저장
    with codecs.open(output_file_path, 'w', encoding=new_encoding) as f:
        f.write(content)

def save_xml(xml_file):
    tree = ET.parse(xml_file)
    tree.write(xml_file, encoding='utf-8')
    return xml_file

def write_xml(xml_file, tree):
    tree.write(xml_file, encoding='utf-8')
    return xml_file

def insert_text_into_tag(xml_file, target_tag: str, insert_tag: str, insert_text: str=None):
    # XML 파일 로드
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 대상 태그를 찾음
    target_elems = root.findall('.//' + target_tag)

    # 대상 태그에 삽입할 태그를 생성하고 내용을 추가
    for target_elem in target_elems:
        insert_elem = ET.Element(insert_tag)
        insert_elem.text = insert_text
        target_elem.insert(0, insert_elem)

    # 수정된 XML 파일 저장
    tree.write(xml_file, encoding='utf-8')
    return xml_file

def replace_specific_tags(xml_file, parent_tag, target_tag, new_content):
    # XML 파일 로드
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 부모 태그를 찾음
    parent_elems = root.findall('.//' + parent_tag)

    # 부모 태그 아래의 특정 태그의 내용을 바꿈
    for parent_elem in parent_elems:
        target_elems = parent_elem.findall(target_tag)
        for target_elem in target_elems:
            target_elem.text = new_content

    # 수정된 XML 파일 저장
    write_xml(xml_file, tree)
    return xml_file

def replace_tag_content(xml_file, target_tag, new_content):
    # XML 파일 로드
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 대상 태그를 찾음
    target_elems = root.findall('.//' + target_tag)

    # 대상 태그의 내용을 바꿈
    for target_elem in target_elems:
        target_elem.text = new_content

    # 수정된 XML 파일 저장
    write_xml(xml_file, tree)
    return xml_file

def replace_tag_first_content(xml_file, target_tag, new_content):
    # XML 파일 로드
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 대상 태그를 찾음
    target_elem = root.find('.//' + target_tag)

    # 대상 태그의 내용을 바꿈
    target_elem.text = new_content

    # 수정된 XML 파일 저장
    write_xml(xml_file, tree)
    return xml_file

def get_tag_content(xml_file, target_tag):
    # XML 파일 로드
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 대상 태그를 찾음
    findall = root.findall(f'.//{target_tag}')
    target_elem = None
    if findall:
        target_elem = findall[0]
        print(f"target_elem: {target_elem}")
        print(f"target_elem: {target_elem.text}")

    # 대상 태그의 내용을 리턴
    # for elem in target_elems:
    if target_elem is not None:
        return target_elem.text

    # 대상 태그가 존재하지 않을 경우 None 리턴
    return None

def get_tag_contents(xml_file, target_tag):
    # XML 파일 로드
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 대상 태그를 찾음
    findall = root.findall(f'.//{target_tag}')
    target_elem = None
    result = []
    if findall:
        # print(findall)
        for target_elem in findall:
            print(target_elem.text)
            result.append(target_elem.text)
        return result
    return None

def remove_tag(xml_file, target_tag):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    parent = None
    for elem in root.iter():
        if elem is not None:
            child = elem.find(target_tag)
            if child is not None:
                parent = elem
                parent.remove(child)
    # 수정된 XML 파일 저장
    tree.write(xml_file, encoding='utf-8')
    return xml_file

def find_tag(xml_file, target_tag):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 대상 태그를 찾아 반환
    for elem in root.iter(target_tag):
        return elem

    # 대상 태그를 찾지 못한 경우 None 반환
    return None

def add_sub(parent, child, text=''):
    obj = ET.SubElement(parent, child)
    obj.text = text
    return obj

def xml_to_dict(element):
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

def search_xml_by_attribute(xml_path, tag_name, attribute_name, attribute_value):
    """
    XML 파일에서 주어진 태그와 속성값을 기반으로 태그를 검색하고 해당 태그의 정보를 반환합니다.

    :param xml_path: XML 파일의 경로
    :param tag_name: 검색하고자 하는 태그명
    :param attribute_name: 검색하고자 하는 속성명
    :param attribute_value: 검색하고자 하는 속성값
    :return: 일치하는 태그의 정보 (태그명, 속성들)
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    results = []

    for elem in root.iter(tag_name):
        if elem.attrib.get(attribute_name) == attribute_value:
            results.append((elem.tag, elem.attrib))

    return results