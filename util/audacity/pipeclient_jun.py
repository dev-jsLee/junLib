# -*- coding: utf-8 -*-
import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.library.junLib import *
from _workplace.util.audacity.pipeclient import PipeClient
import time

if sys.version_info[0] < 3 and sys.version_info[1] < 7:
    sys.exit('PipeClient Error: Python 2.7 or later required')

# Platform specific constants
if sys.platform == 'win32':
    WRITE_NAME = '\\\\.\\pipe\\ToSrvPipe'
    READ_NAME = '\\\\.\\pipe\\FromSrvPipe'
    EOL = '\r\n\0'
else:
    # Linux or Mac
    PIPE_BASE = '/tmp/audacity_script_pipe.'
    WRITE_NAME = PIPE_BASE + 'to.' + str(os.getuid())
    READ_NAME = PIPE_BASE + 'from.' + str(os.getuid())
    EOL = '\n'

class PipeClient_jun(PipeClient):

    def __init__(self, enc='utf-8'):
        super().__init__(enc)
        self.project_name = None
        self.project_path = None
        self.txt_file_path = None

    def save_to_label(self, txt_file_path=None):
        self.txt_file_path = txt_file_path or self.txt_file_path
        self.write(f'ExportLabels: FileName={self.txt_file_path}')
    
    def read_json(self):
        text = self.read()
        time.sleep(5)  # 약간의 지연 시간을 둡니다.
        print(text)
        input("Enter to continue.")
        return text

    def set_txt_file_path(self, txt_file_path):
        self.txt_file_path = txt_file_path

    def save_project(self, path=None):
        if path:
            # 지정된 경로에 프로젝트 저장
            self.write(f"SaveProject2: Path={path}\n")
            time.sleep(3)  # 약간의 지연 시간을 둡니다.
            self.project_path = path
            return self
        # else:
        #     # 현재 프로젝트 저장
        #     self.write("SaveProject2:\n")
        
        #     return self.write("GetProject:\n")
    def get_project(self):
        return self.project_path

    def set_project_name(self, project_name:str=None): # type: ignore
        if project_name:
            self.write(f'SetProject: Name="{project_name}"')
            self.project_name = project_name
        return self
    
    def get_project_name(self):
        return self.project_name

    def delete_all(self):
        self.write(f"SelAllTracks")
        self.write(f"RemoveTracks")

    def exit(self):
        self.write(f"Exit")

    def _write_pipe_open(self):
        """Open _write_pipe."""
        if self.enc:
            self._write_pipe = open(WRITE_NAME, 'w', newline='', encoding=self.enc)
        else:
            self._write_pipe = open(WRITE_NAME, 'w', newline='', encoding='utf-8')
