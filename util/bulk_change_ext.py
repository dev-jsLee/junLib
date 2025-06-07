import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *

def run():
    folder_path = strip_quotes(input('Enter folder path: '))
    file_paths = get_files_path_at_all(folder_path)
    for file_path in file_paths:
        renamed_file_path = change_extension(file_path, 'jpg')
        move_file(file_path, renamed_file_path)

if __name__ == "__main__" :
    run()