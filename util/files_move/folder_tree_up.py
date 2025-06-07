# -*- coding: utf-8 -*-
import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.library.junLib import *

import os
import shutil
import time

class FolderLifter:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def lift_folders(self, lift_file:bool=True):
        # 입력받은 폴더 내의 모든 하위 폴더를 가져옵니다.
        subfolders = [f.path for f in os.scandir(self.base_path) if f.is_dir()]

        for subfolder in subfolders:
            print("process ", subfolder)
            if lift_file:
                inner_files = [f.path for f in os.scandir(subfolder) if f.is_file()]
                for inner_file in inner_files:
                    file_basename = os.path.basename(inner_file)
                    new_path = join_folder_path(self.base_path, file_basename)
                    move_file(inner_file, new_path)
            # 각 하위 폴더 내의 폴더들을 가져옵니다.
            inner_subfolders = [f.path for f in os.scandir(subfolder) if f.is_dir()]

            for inner_subfolder in inner_subfolders:
                # 하위 폴더의 이름을 가져옵니다.
                inner_subfolder_name = os.path.basename(inner_subfolder)
                # 새로운 경로를 생성합니다.
                new_path = os.path.join(self.base_path, inner_subfolder_name)

                # 해당 폴더가 이미 존재하는지 확인하고, 없으면 폴더를 생성합니다.
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                    print(new_path)

                # 파일들을 새로운 폴더로 옮깁니다.
                for item in os.listdir(inner_subfolder):
                    s = os.path.join(inner_subfolder, item)
                    d = os.path.join(new_path, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)

                # 옮긴 후 원래의 폴더를 삭제합니다.
                try:
                    shutil.rmtree(inner_subfolder)
                except:
                    time.sleep(3)
                    shutil.rmtree(inner_subfolder)
                    

            # 모든 파일을 옮긴 후 상위 폴더도 삭제합니다.
            if lift_file:
                os.rmdir(subfolder)
            else:
                remove_empty_folders(self.base_path)

if __name__ == "__main__":
    base_path = strip_quotes(input("폴더 경로를 입력하세요: "))
    lifter = FolderLifter(base_path)
    lifter.lift_folders()
    print("폴더 이동이 완료되었습니다.")
