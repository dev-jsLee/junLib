import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *

def delete_files_except_xml_mp4(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()

            if file_extension != ".xml" and file_extension != ".mp4":
                os.remove(file_path)
def run():
    # 사용 예시
    folder_path = strip_quotes(input('Enter folder path: '))
    delete_files_except_xml_mp4(folder_path)
if __name__ == "__main__":
    run()