"""
XML 파일 처리를 위한 모듈

이 모듈은 XML 파일을 처리하기 위한 클래스와 유틸리티 함수들을 제공합니다.
"""

from .XMLHandler import (
    change_xml_encoding,
    save_xml,
    write_xml,
    insert_text_into_tag,
    replace_specific_tags,
    replace_tag_content,
    replace_tag_first_content,
    get_tag_content,
    get_tag_contents,
    remove_tag,
    find_tag,
    add_sub,
    xml_to_dict,
    search_xml_by_attribute
)

from .XMLValidator import XMLController, XMLMaker
from .xml_utils import (
    write_xsd_to_file,
    generate_xsd_from_xml_file,
    generate_xsd_from_xml_string,
    generate_xsd_element
)

__all__ = [
    # XMLHandler 함수들
    'change_xml_encoding',
    'save_xml',
    'write_xml',
    'insert_text_into_tag',
    'replace_specific_tags',
    'replace_tag_content',
    'replace_tag_first_content',
    'get_tag_content',
    'get_tag_contents',
    'remove_tag',
    'find_tag',
    'add_sub',
    'xml_to_dict',
    'search_xml_by_attribute',
    
    # XMLValidator 클래스들
    'XMLController',
    'XMLMaker',
    
    # utils 함수들
    'write_xsd_to_file',
    'generate_xsd_from_xml_file',
    'generate_xsd_from_xml_string',
    'generate_xsd_element'
]
