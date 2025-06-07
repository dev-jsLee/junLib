"""
junLib - 파일 및 데이터 조작을 위한 유틸리티 함수 모음
"""

import importlib.metadata

# 핵심 모듈 임포트
from .xml import (
    XMLController,
    XMLMaker,
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

from .csv import (
    CSVHandler,
    read_csv_and_get_rows,
    write_rows,
    find_column_index,
    add_column_names,
    add_row_numbers,
    dict_to_csv,
    search_and_replace_content
)

from .video import VideoHandler, AudioHandler
from .file import FileHandler
from .util.datetime import format_time, format_time_with_ms

try:
    __version__ = importlib.metadata.version("junLib")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.1.1"  # fallback version

__author__ = "jslee7518"
__email__ = "jslee7518@gmail.com"

__all__ = [
    # XML 관련
    'XMLController',
    'XMLMaker',
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
    
    # CSV 관련
    'CSVHandler',
    'read_csv_and_get_rows',
    'write_rows',
    'find_column_index',
    'add_column_names',
    'add_row_numbers',
    'dict_to_csv',
    'search_and_replace_content',
    
    # 비디오 관련
    'VideoHandler',
    'AudioHandler',
    
    # 파일 시스템 관련
    'FileHandler',
    
    # 유틸리티
    'format_time',
    'format_time_with_ms'
]
