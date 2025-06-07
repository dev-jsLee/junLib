import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *

def run():
    folder_path = strip_quotes(input('Enter folder path : '))
    remove_empty_folders(folder_path)
    print("done.")

    # sub_paths = sub_path(folder_path)
    # for subpath in sub_paths:
    #     if len(sub_path_dict(subpath))>0:
    #         print(sub_path_dict(subpath)['annotated_images'])
    #         print(sub_path_dict(subpath)['delete_xml'])
    #         move_folder(sub_path_dict(subpath)['annotated_images'], join_folder_path(folder_path, 'delete'))
    #         move_folder(sub_path_dict(subpath)['delete_xml'], join_folder_path(folder_path, 'delete'))
    #     pass
    # pass

if __name__ == "__main__":
    run()