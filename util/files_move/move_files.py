# move_files.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *

def process(folder_path):
    mp4_files = get_files_in_folder_via_ext(folder_path, 'mp4')
    for file_name_and_ext in mp4_files:
        jpg_files = get_files_path_in_folder_via_ext(folder_path, 'jpg')
        mp4_file_path = join_folder_path(folder_path, file_name_and_ext)
        file_name, ext = os.path.splitext(basename(file_name_and_ext))
        if path_exist(mp4_file_path):
            print(f"mp4_file_path: {mp4_file_path}")
            create_folder(join_folder_path(folder_path, file_name))
            # move_file(mp4_file_path, join_folder_path(folder_path, file_name, file_name_and_ext))
            shutil.move(mp4_file_path, join_folder_path(folder_path, file_name))
            for jpg_file_path in jpg_files:
                jpg_file_name, ext = os.path.splitext(basename(jpg_file_path))
                if str(jpg_file_name).startswith(file_name):
                    move_file(jpg_file_path, join_folder_path(folder_path, file_name, os.path.basename(xml_file)))
            xml_file = change_extension(mp4_file_path, 'xml')
            if path_exist(xml_file):
                print(f"xml_file: {xml_file}")
                move_file(xml_file, join_folder_path(folder_path, file_name, os.path.basename(xml_file)))
    return folder_path

def process_underbar(folder_path=''):
    # mp4_files = get_files_in_folder_via_ext(folder_path, 'mp4')
    files = get_files_path_at_all(folder_path)
    for file_path in files:
        file_name, ext = os.path.splitext(basename(file_path))
        target_folder = join_folder_path(folder_path, file_name[:20])
        create_folder(target_folder)
        shutil.move(file_path, target_folder)
    return folder_path


def run():
    folder_path = strip_quotes(input('Enter Folder path: '))
    print(f"작업완료 : {process_underbar(folder_path)}")
    
if __name__ == "__main__":
    run()