# -*- coding: utf-8 -*-
import xml
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os
import sys
from collections import Counter
import json
from . import junLib
from . import junLib_xml
from . import junLib_json

class XmlToJsonConverter:
    def __init__(self, xml_file_path):
        # change_xml_encoding(xml_file_path)
        self.tree = ET.parse(xml_file_path)
        self.root = self.tree.getroot()

    def convert_to_json(self, element=None)->dict:
        if element is None:
            element = self.root

        json_data = {}
        # 태그의 텍스트 값이 있으면 __text__ 키로 저장
        if element.text and element.text.strip():
            json_data['__text__'] = element.text.strip()

        # 태그의 속성이 있으면 해당 속성을 저장
        for key, value in element.attrib.items():
            json_data[key] = value

        # 자식 태그가 있으면 재귀적으로 호출하여 저장
        for child in element:
            child_data = self.convert_to_json(child)
            if child.tag not in json_data:
                json_data[child.tag] = child_data
            else:
                if not isinstance(json_data[child.tag], list):
                    json_data[child.tag] = [json_data[child.tag]]
                json_data[child.tag].append(child_data)

        return json_data

    def get_json(self):
        return self.convert_to_json()

    def remove_tag(self, tag_name, data=None):
        """
        특정 태그(키)를 제거하는 함수
        """
        if data is None:
            data = self.get_json()

        if tag_name in data:
            del data[tag_name]

        for key, value in data.items():
            if isinstance(value, dict):
                self.remove_tag(tag_name, value)
            elif isinstance(value, list):
                for item in value:
                    self.remove_tag(tag_name, item)

        return data

    def get_text_statistics(self, tag_name):
        """
        특정 태그의 '__text__' 값의 통계를 반환하는 메서드
        """
        json_data = self.get_json()
        text_values = self._extract_text_values(json_data, tag_name)
        return dict(Counter(text_values))

    def _extract_text_values(self, data, tag_name):
        """
        재귀적으로 특정 태그의 '__text__' 값을 추출하는 내부 메서드
        """
        text_values = []

        if isinstance(data, dict):
            if data.get(tag_name):
                # data[tag_name]이 딕셔너리인지 확인
                if isinstance(data[tag_name], dict):
                    text_value = data[tag_name].get('__text__')
                    if text_value:
                        text_values.append(text_value)
                # data[tag_name]이 리스트인 경우
                elif isinstance(data[tag_name], list):
                    for item in data[tag_name]:
                        if isinstance(item, dict) and '__text__' in item:
                            text_values.append(item['__text__'])
            for key, value in data.items():
                text_values.extend(self._extract_text_values(value, tag_name))
        elif isinstance(data, list):
            for item in data:
                text_values.extend(self._extract_text_values(item, tag_name))
        return text_values

def insert_into_dict(dictionary, key, value, index):
    items = list(dictionary.items())
    items.insert(index, (key, value))
    return dict(items)

class JsonToXmlConverter:
    def __init__(self, json_data:dict, root_name='annotation'):
        self.json_data = json_data
        self.root_name = root_name

    def prettify_xml(self, file_path):
        dom = minidom.parse(file_path)

        # XML을 들여쓰기 형식으로 변환한 후, 빈 줄을 제거
        xml_str = dom.toprettyxml(indent="    ")
        xml_lines = xml_str.splitlines()
        non_empty_lines = [line for line in xml_lines if line.strip()]
        result = "\n".join(non_empty_lines)

        # XML 파일로 저장 (indent 옵션으로 들여쓰기)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(result)

    def convert_to_xml(self):
        root = ET.Element(self.root_name)
        self._add_children(root, self.json_data)
        return ET.ElementTree(root)

    def _add_children(self, parent_element:ET.Element, data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    # 키의 값이 리스트인 경우, 여러 개의 키값 태그를 생성하여 자식 요소로 추가
                    for item in value:
                        child = ET.Element(key)
                        self._add_children(child, item)
                        parent_element.append(child)
                elif isinstance(value, dict):
                    # value가 dict인 경우, 새로운 요소를 생성하고 재귀적으로 호출하여 자식 요소를 추가
                    child = ET.Element(key)
                    self._add_children(child, value)
                    parent_element.append(child)
                else:
                    # value가 dict가 아닌 경우, key가 __text__라면 부모 태그의 텍스트를 해당 값으로 설정
                    if str(key) == '__text__':
                        if isinstance(value, str):
                            parent_element.text = value
                        else:
                            parent_element.text = str(value)
                    else:
                        # key가 __text__가 아니라면 해당 태그의 속성으로 입력
                        parent_element.set(key, str(value))

        elif isinstance(data, list):
            for item in data:
                # list의 각 요소에 대해 재귀적으로 호출하여 자식 요소를 추가
                child = ET.Element(parent_element.tag)
                self._add_children(child, item)
                parent_element.append(child)
        else:
            parent_element.text = str(data)
    
    def save_to_xml_file(self, file_path):
        xml_tree = self.convert_to_xml()
        xml_tree.write(file_path, encoding='utf-8', xml_declaration=True)
        self.prettify_xml(file_path)

class JsonToDictConverter:
    
    def __init__(self, json_file_path=None, xml_file_path=None) -> None:
        if json_file_path: self.load_json_file(json_file_path)
        if xml_file_path: self.json_data = XmlToJsonConverter(xml_file_path=xml_file_path).convert_to_json()
        # self.json_data = None

    def load_json_file(self, json_file_path, encoding='utf-8'):
        self.json_file_path = json_file_path or self.json_file_path
        if str(os.path.splitext(self.json_file_path)[1]).__contains__('json'):
            try:
                with open(self.json_file_path, 'r', encoding=encoding) as json_file:
                    self.json_data = json.load(json_file)
            except Exception as e:
                print(f'error {e}')
                return self.load_json_file_no_encoding(self.json_file_path)
        else:
            print(f"{json_file_path} is not a json file.")
        return self

    def load_json_file_no_encoding(self, json_file_path):
        self.json_file_path = json_file_path or self.json_file_path
        if str(os.path.splitext(self.json_file_path)[1]).__contains__('json'):
            with open(self.json_file_path, 'r') as json_file:
                self.json_data = json.load(json_file)
        else:
            print(f"{json_file_path} is not a json file.")
        return self

if __name__ == "__main__":
    # 예시 JSON 데이터
    # speaker
    # mp4, mp3, xml, txt
    # E20200907_00004_007_02.xml
    json_data_speaker = {
        'filename':{
            '__text__': 'E20200907_00004_007_02.mp3'
        },
        'label':{
            'starttime':{
                '__text__': '392.000'   # 위 filename 기준, speaker가 말한 타임스탬프
            },
            'endtime': {
                '__text__': '416.000'   # 위 filename 기준, speaker가 말한 타임스탬프
            },
            'speaker': {
                '__text__': 'jo_sun_jeong'# 위 filename 기준, speaker 정보
            }
        }
    }

    # speaker
    # txt
    speaker_data = """
    362.00\t394.00\tjo_sun_jeong\n
    392.00\t416.00\tjo_sun_jeong\n
    470.00\t475.00\tkwon_seung_hyeok\n
    473.00\t501.00\tkwon_seung_hyeok
    """

    # speech
    # mp4, xml
    # 200904_01_032_02_003.xml
    json_data_speech = {
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
            '__text__': '362.000'
        },
        'endtime_origin':{
            '__text__': '394.000'
        },
        'name':{
            '__text__': 'jo_sun_jeong'
        },
        'text':{
            '__text__': '교수과 러 교수들, 박사들을 부르시어 개혁사업과 관련한 기증한 교실을 주셨습니다.'
        },
        'label':{
            'starttime':{
                '__text__': '392.000'
            },
            'endtime': {
                '__text__': '416.000'
            },
            'word': {
                '__text__': 'jo_sun_jeong'
            }
        }
    }

    # speech
    # 200904_01_032_02_003.xml
    json_data_speech = {
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
            '__text__': '362.000'
        },
        'endtime_origin':{
            '__text__': '394.000'
        },
        'name':{
            '__text__': 'jo_sun_jeong'
        },
        'text':{
            '__text__': '교수과 러 교수들, 박사들을 부르시어 개혁사업과 관련한 기증한 교실을 주셨습니다.'
        },
        'label':{
            'starttime':{
                '__text__': '392.000'
            },
            'endtime': {
                '__text__': '416.00'
            },
            'word': {
                '__text__': 'jo_sun_jeong'
            }
        }
    }

    # emotion
    # 200904_01_032_02_003.xml
    json_data_emotion = {
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
        # 'label':{
        #     'starttime':{
        #         '__text__': '392.000'
        #     },
        #     'endtime': {
        #         '__text__': '416.00'
        #     },
        #     'word': {
        #         '__text__': 'jo_sun_jeong'
        #     }
        # }
    }

    json_data_face = {
        'folder': {
            '__text__': 'Z:\\final working\\202009\\emotion_need_face\\neutral\\aeng_keo_nam_03'
        },
        'filename':{
            '__text__': 'E20200907_00009_02474'
        },
        # 'filename_origin':{
        #     '__text__': 'E20200907_00009.mp4'
        # },
        'object':{
            'filename':{
                '__text__':'E20200907_00008_030_99-223_230.5-neutral_aeng_keo_nam_03_00000.jpg'
            },
            'name':{
                '__text__': 'aeng_keo_nam_03'
            },
            'size':{
                'width':{'__text__':'1920'},
                'height':{'__text__':'1080'},
                'depth':{'__text__':'3'}
            },
            'name':{'__text__':'aeng_keo_yeo_03'},
            'bndbox':{
                'xmin':{'__text__':'257'},
                'ymin':{'__text__':'183'},
                'xmax':{'__text__':'322'},
                'ymax':{'__text__':'272'},
                'width':{'__text__':'65'},
                'height':{'__text__':'89'},
            },
            'landmark':{
                'Leye':{
                    'x':{'__text__':'298'},
                    'y':{'__text__':'206'}
                },
                'Reye':{
                    'x':{'__text__':'310'},
                    'y':{'__text__':'206'}
                },
                'Nose':{
                    'x':{'__text__':'318'},
                    'y':{'__text__':'226'}
                },
                'Lmouth':{
                    'x':{'__text__':'308'},
                    'y':{'__text__':'246'}
                },
                'Rmouth':{
                    'x':{'__text__':'316'},
                    'y':{'__text__':'247'}
                }
            },
            'frontal':{'__text__':'True'},
            'occlusion':{'__text__':'False'},
            'important':{'__text__': 'aeng_keo'}
        }
    }

    # JSON을 XML로 변환하여 파일로 저장
    # xml_file_path = strip_quotes(input('Enter xml file path : '))
    # obj = XmlToJsonConverter(xml_file_path)
    # json_data_ = obj.convert_to_json()
    # write_to_json(json_data_, rename(xml_file_path, new_extension='json'))

    # converter = JsonToXmlConverter(json_data_face, root_name="annotation")
    # converter.save_to_xml_file("output.xml")

    # json파일을 xml로 저장
    # json_file_path = strip_quotes(input('Enter json file path : '))
    # obj = JsonToDictConverter(json_file_path=json_file_path)
    # json_data = obj.load_json_file(json_file_path=json_file_path).json_data
    # obj = JsonToXmlConverter(json_data=json_data)
    # obj.save_to_xml_file(rename(json_file_path, new_extension='xml'))