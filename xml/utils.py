"""
XML 파일 처리를 위한 유틸리티 함수들
"""
# -*- coding: utf-8 -*-
import os
import sys
import xml.etree.ElementTree as ET
from .. import junLib

def write_xsd_to_file(xsd_string, file_name):
    try:
        with open(file_name, 'w') as xsd_file:
            xsd_file.write(xsd_string)
        print(f"XSD 파일 '{file_name}'이 성공적으로 생성되었습니다.")
    except IOError:
        print(f"파일 '{file_name}'을(를) 생성하는 데 오류가 발생했습니다.")

def generate_xsd_from_xml_file(xml_file_path):
    try:
        # XML 파일 읽기
        with open(xml_file_path, 'r', encoding='utf-8') as xml_file:
            xml_string = xml_file.read()

        # XML 파싱
        xml_tree = ET.fromstring(xml_string)

        # XSD 생성
        xsd = f'<xs:element name="{xml_tree.tag}">\n'
        xsd += generate_xsd_element(xml_tree)
        xsd += "</xs:element>"

        return xsd
    except (IOError, ET.ParseError):
        return None

def generate_xsd_from_xml_string(xml_string):
    try:
        # XML 파싱
        xml_tree = ET.fromstring(xml_string)

        # XSD 생성
        xsd = f'<xs:element name="{xml_tree.tag}">\n'
        xsd += generate_xsd_element(xml_tree)
        xsd += "</xs:element>"

        return xsd
    except ET.ParseError:
        return None

def generate_xsd_element(xml_element):
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