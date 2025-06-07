import os
import shutil
from __init__ import *
from _workplace.library.junLib import *

def move_specific_files_with_tree(src_folder, dst_folder, extensions:list):
    # 새로운 폴더를 생성합니다.
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
        
    # 기존 폴더의 파일과 서브폴더를 순회하면서 작업을 수행합니다.
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            # 특정 확장자를 가진 파일만을 대상으로 합니다.
            extension = file.split('.')[-1]
            if extension in extensions:
                # 원본 파일의 전체 경로를 구합니다.
                file_path = os.path.join(root, file)
                
                # 새로운 경로를 구성합니다. 이 때 폴더 트리 구조를 유지합니다.
                relative_path = os.path.relpath(root, src_folder)
                new_folder = os.path.join(dst_folder, relative_path)
                if not os.path.exists(new_folder):
                    os.makedirs(new_folder)
                
                # 파일을 새로운 경로로 이동합니다.
                shutil.move(file_path, new_folder)

if __name__ == "__main__":
    origin_folder_path = strip_quotes(input("Enter origin folder path :"))
    # if not path_exist(rename(origin_folder_path, suffix='_backup_auto')): copy_and_rename_folder(origin_folder_path, rename(origin_folder_path, suffix='_backup_auto'))
    dst_folder_path = rename(origin_folder_path, suffix='_t')
    targets = [
        'json', 
        'bak', 
        'txt',
        'mp3',
        ]
    move_specific_files_with_tree(origin_folder_path, dst_folder_path, targets)