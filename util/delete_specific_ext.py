import shutil
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *

def move_files_to_delete_folder(folder_path, target='image'):
    # "delete" 폴더가 없다면 생성
    delete_folder = os.path.join(folder_path, "delete")
    if not os.path.exists(delete_folder):
        os.mkdir(delete_folder)

    # 폴더 내의 모든 파일 및 폴더 검사
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # 타겟 및 파일이 이미지 파일인지 확인
            if target == 'image':
                is_image_file(file_path, delete_folder)
            elif target == 'video':
                is_video_file(file_path, delete_folder)
            elif target == 'trash':
                is_trash_file(file_path, delete_folder)

def is_image_file(file_path, delete_folder):
    file_name = os.path.basename(file_path)
    # 파일 확장자 확인
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
    ext = os.path.splitext(file_name)[1].lower()
    if ext in image_extensions:
        # 이미지 파일을 "delete" 폴더로 이동
        new_file_path = os.path.join(delete_folder, file_name)
        shutil.move(file_path, new_file_path)
        print(f"Moved {file_name} to delete folder.")

def is_trash_file(file_path, delete_folder):
    file_name = os.path.basename(file_path)
    # 파일 확장자 확인
    image_extensions = [
        ".bak", 
        ".fbak",
        # ".wav", 
        # ".txt", 
        # ".json", 
        # '.xml', 
        ".backup",
    ]
    ext = os.path.splitext(file_name)[1].lower()
    if ext in image_extensions:
        # 이미지 파일을 "delete" 폴더로 이동
        new_file_path = os.path.join(delete_folder, file_name)
        shutil.move(file_path, new_file_path)
        print(f"Moved {file_name} to delete folder.")

def is_video_file(file_path, delete_folder):
    file_name = os.path.basename(file_path)
    # 파일 확장자 확인
    image_extensions = [".mp4"]
    ext = os.path.splitext(file_name)[1].lower()
    if ext in image_extensions:
        # 이미지 파일을 "delete" 폴더로 이동
        new_file_path = os.path.join(delete_folder, file_name)
        shutil.move(file_path, new_file_path)
        print(f"Moved {file_name} to delete folder.")

def run(folder_path=None, ext:str='fbak'):
    folder_path = folder_path or strip_quotes(input('Enter Folder path: '))
    # move_files_to_delete_folder(folder_path, 'video')
    # move_files_to_delete_folder(folder_path, 'trash')
    files = get_files_path_in_folder_via_ext(folder_path, ext, True)
    for i, file_path in enumerate(files):
        delete_file(file_path)

if __name__ == "__main__":
    run()