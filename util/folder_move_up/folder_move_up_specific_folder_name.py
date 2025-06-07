# -*- coding: utf-8 -*-
import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.util.files_move import move_folder_tree
from _workplace.library.junLib import *
import shutil

def move_sub_sub_contents(target):
    # target 폴더 내의 모든 하위 폴더를 탐색
    for sub in os.listdir(target):
        sub_path = os.path.join(target, sub)
        
        # sub가 폴더인 경우만 처리
        if os.path.isdir(sub_path):
            # sub의 하위 폴더 및 파일의 경로를 탐색
            for dirpath, dirnames, filenames in os.walk(sub_path, topdown=False):
                # 파일 이동
                for filename in filenames:
                    src = os.path.join(dirpath, filename)
                    dst = src.replace(f'/{sub}/', '/')
                    if not os.path.exists(dst):
                        shutil.move(src, dst)
                    else:
                        print(f"파일이 이미 존재합니다: {dst}")
                
                # 폴더 이동
                for dirname in dirnames:
                    src = os.path.join(dirpath, dirname)
                    dst = src.replace(f'/{sub}/', '/')
                    if not os.path.exists(dst):
                        shutil.move(src, dst)
                    else:
                        print(f"폴더가 이미 존재합니다: {dst}")
                    
            # sub 폴더 삭제
            if not os.listdir(sub_path):  # 폴더가 비어 있는지 확인
                os.rmdir(sub_path)
            else:
                pass
                # shutil.rmtree(sub_path)  # 폴더 내의 모든 내용을 삭제

if __name__ == '__main__':
    # 사용 예
    # target_path = "/path/to/target"  # 원하는 경로로 변경하세요.
    target_path = strip_quotes(input('Enter folder path : '))
    subs = get_dir_sub_folder_path(target_path)
    for i, sub in enumerate(subs):
        merged_folder_path = join_folder_path(sub, '_merged')
        move_folder_tree.move_folder_structure(sub, join_folder_path(target_path, '_merged'))
