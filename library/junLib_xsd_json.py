# -*- coding: utf-8 -*-
import os
import sys
from __init__ import source_code_path
sys.path.append(source_code_path)
from _workplace.library.junLib import *
from _workplace.library.junLib_xml_class_json import *
import xml.etree.ElementTree as ET

class JsonToXsdConverter:
    def __init__(self, json_data, root_name=None):
        self.json_data = json_data
        self.root_name = root_name or "annotation"

    def convert_to_xsd(self):
        root = ET.Element("xs:element", name=self.root_name)
        child_type = ET.SubElement(root, "xs:complexType")
        sequence = ET.SubElement(child_type, "xs:sequence")
        self._add_xsd_elements(sequence, self.json_data)
        return ET.ElementTree(root)

    def _add_xsd_elements(self, parent_element, data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == '__text__':
                    continue  # '__text__'는 XSD에서 처리하지 않습니다.
                child = ET.Element("xs:element", name=key)
                if isinstance(value, list):
                    # list의 경우, 해당 요소가 반복될 수 있음을 나타내기 위해 maxOccurs="unbounded"를 설정
                    child.set("maxOccurs", "unbounded")
                    if len(value) > 0:
                        child_type = ET.SubElement(child, "xs:complexType")
                        sequence = ET.SubElement(child_type, "xs:sequence")
                        self._add_xsd_elements(sequence, value[0])  # 첫 번째 요소를 기준으로 XSD를 생성
                elif isinstance(value, dict):
                    # value가 dict인 경우, 새로운 요소를 생성하고 재귀적으로 호출하여 자식 요소를 추가
                    child_type = ET.SubElement(child, "xs:complexType")
                    sequence = ET.SubElement(child_type, "xs:sequence")
                    self._add_xsd_elements(sequence, value)
                else:
                    # value가 dict가 아닌 경우, 해당 키를 속성으로 추가
                    child = ET.Element("xs:attribute", name=key)
                    child.set("type", "xs:string")
                parent_element.append(child)

        else:
            # 기본 데이터 유형 (문자열, 숫자 등)에 대한 처리
            parent_element.set("type", "xs:string")

    def save_to_xsd_file(self, file_path):
        xsd_root = self.get_xsd_root_element()
        xsd_str = ET.tostring(xsd_root, encoding='utf-8').decode('utf-8')

        # 네임스페이스 선언 추가
        xsd_str = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">\n' + \
                xsd_str + \
                '</xs:schema>'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(xsd_str)

        self.prettify_xsd(file_path)

    def get_xsd_root_element(self):
        return self.convert_to_xsd().getroot()

    def prettify_xsd(self, file_path):
        dom = minidom.parse(file_path)

        # XSD를 들여쓰기 형식으로 변환한 후, 빈 줄을 제거
        xsd_str = dom.toprettyxml(indent="    ")
        xsd_lines = xsd_str.splitlines()
        non_empty_lines = [line for line in xsd_lines if line.strip() and not line.strip().startswith('<?xml version="1.0" ?>')]
        result = "\n".join(non_empty_lines)

        # XSD 파일로 저장 (indent 옵션으로 들여쓰기)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(result)
def run():
    target_xml_file_path = strip_quotes(input('Enter target xml file : '))
    obj = XmlToJsonConverter(target_xml_file_path)
    json_data = obj.convert_to_json()
    print(json_data)
    obj = JsonToXsdConverter(json_data, 'annotation')
    obj.save_to_xsd_file(rename(target_xml_file_path, new_extension='xsd'))

def run_example():
    # 예시 JSON 데이터
    # emotion
    # 200904_01_032_02_003.xml
    json_data_example = {
        'folder':{
            '__text__':'Z:\\202009\\final working\\speech\\_200904_speech_last'
            },
        'filename':{
            '__text__': 'E20200907_00004_007_02_006'
        },
        'filename_origin':{
            '__text__': 'E20200907_00004.mp4'
        },
        'starttime_origin':{
            '__text__': '362.000'   # filename_origin 기준 시작 타임스탬프  # 소숫점 3자리
        },
        'endtime_origin':{
            '__text__': '394.000'   # filename_origin 기준 시작 타임스탬프  # 소숫점 3자리
        },
        'name':{
            '__text__':'jo_sun_jeong'
        },
        'text':{
            '__text__': '교수과 러 교수들, 박사들을 부르시어 개혁사업과 관련한 기증한 교실을 주셨습니다.'
        },
        'labels': [
            {
                'starttime': {
                    '__text__': '392.000'   # 소숫점 3자리
                },
                'endtime': {
                    '__text__': '416.000'   # 소숫점 3자리
                },
                'word': {
                    '__text__': 'jo_sun_jeong'
                }
            },
            {
                'starttime': {
                    '__text__': '392.000'
                },
                'endtime': {
                    '__text__': '416.00'
                },
                'word': {
                    '__text__': 'jo_sun_jeong'
                }
            }
        ]
    }

    # JSON을 XSD로 변환하여 파일로 저장
    converter = JsonToXsdConverter(json_data_example, root_name="annotation")
    converter.save_to_xsd_file("output.xsd")


# 예제 사용
if __name__ == "__main__":
    run()
