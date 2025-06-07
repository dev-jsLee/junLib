# -*- coding: utf-8 -*-
import os
import sys
current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)
_workplace_folder_path = current_directory

while(True):
    if os.path.basename(_workplace_folder_path) == '_workplace':
        break
    else:
        _workplace_folder_path = os.path.dirname(_workplace_folder_path)
        continue
source_code_path = os.path.dirname(_workplace_folder_path)
_gitlab_path = os.path.dirname(source_code_path)
root_folder_path = os.path.dirname(_gitlab_path)
sys.path.append(source_code_path)
from _workplace.library.junLib import *
from _workplace.util.audacity.pipeclient import PipeClient
from _workplace.util.audacity.pipeclient_jun import PipeClient_jun
from _workplace.util.media_files_control import transfer_mp4_to_mp3 as transfer
import xml.etree.ElementTree as ET

ffmpeg_path = join_folder_path(root_folder_path, '_resource', 'ffmpeg-n5.1-latest-win64-lgpl-5.1', 'bin') + '\\ffmpeg'

import sqlite3

def extract_labels_from_aup3(aup3_filename, output_txt_filename):
    # SQLite 데이터베이스 연결
    conn = sqlite3.connect(aup3_filename)
    cursor = conn.cursor()

    # 레이블 정보를 저장할 리스트
    labels = []

    # 레이블 정보 조회 (SQL 쿼리는 .aup3 파일의 구조에 따라 조정이 필요할 수 있습니다)
    cursor.execute("SELECT start_time, end_time, title FROM labels")
    for row in cursor.fetchall():
        start_time, end_time, title = row
        labels.append((start_time, end_time, title))

    # 데이터베이스 연결 종료
    conn.close()

    # 레이블 정보를 .txt 파일로 저장
    if path_exist(output_txt_filename):
        copy_and_rename_file(output_txt_filename, rename(output_txt_filename, new_extension='txt.bak'))
        delete_file(output_txt_filename)
    with open(output_txt_filename, 'w', encoding='utf-8') as f:
        for label in labels:
            f.write(f"{label[0]}\t{label[1]}\t{label[2]}\n")

def save(client, aup_file_path=None):
    # .aup 파일 경로를 사용자로부터 입력받음
    # obj = PipeClient_jun()
    # obj.save_project()
    aup_file_path = aup_file_path or strip_quotes(input("Enter the path to your .aup file: "))
    output_txt_filename = rename(aup_file_path, new_extension=".txt")

    # 레이블 정보 추출 및 저장
    extract_labels_from_aup3(aup_file_path, output_txt_filename)

    # 원본 .aup 파일 삭제
    os.remove(aup_file_path)

def run(client=None, aup_file_path=None):
    client = client or PipeClient()
    save(client=client, aup_file_path=aup_file_path)

if __name__ == "__main__":
    run()