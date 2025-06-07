"""
XML 파일 처리를 위한 핸들러 클래스
"""
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

class XMLHandler:
    """XML 파일 처리를 위한 핸들러 클래스"""
    
    def __init__(self, file_path=None):
        """
        Args:
            file_path (str, optional): XML 파일 경로
        """
        self.file_path = file_path
        self.tree = None
        self.root = None
        if file_path:
            self.load(file_path)
    
    def load(self, file_path):
        """XML 파일을 로드합니다."""
        self.file_path = file_path
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()
        return self
    
    def save(self, file_path=None):
        """XML 파일을 저장합니다."""
        if file_path:
            self.file_path = file_path
        if self.tree:
            self.tree.write(self.file_path, encoding='utf-8', xml_declaration=True)
        return self
    
    def prettify(self, file_path=None):
        """XML 파일을 보기 좋게 포맷팅합니다."""
        if file_path:
            self.file_path = file_path
        dom = minidom.parse(self.file_path)
        pretty_xml = dom.toprettyxml(indent="    ")
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        return self 