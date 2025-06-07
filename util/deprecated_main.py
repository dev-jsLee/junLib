# main.py
# 화자인식, 구화인식을 기준으로 나뉜 영상 폴더의 방송일자 폴더를 입력하면
# 작업한 영상의 총길이를 텍스트 파일로 출력해주는 코드
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *
from _workplace.util import total_length_by_broadcast as br
from _workplace.util import total_length_parent_folder as pf

if __name__ == "__main__":
    current_parent_path = strip_quotes(input("Enter the Folder Path: "))
    for root, dirs, files in os.walk(current_parent_path):
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            output_file = br.run_subdir(folder_path)
            if output_file:
                print(f'파일 출력 완료: {folder_path} , {output_file}')
    pf.run(current_parent_path)