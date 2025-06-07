# -*- coding: utf-8 -*-
import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.library.junLib import *
import shutil

def move_subfolder_contents(root: str, input_name: str):
    """
    Move all the contents of subdirectories inside the root directory to a new folder.
    
    Args:
    - root (str): The path of the root directory.
    - input_name (str): The name of the new folder to be created inside each subdirectory.
    
    """
    if not os.path.exists(root) or not os.path.isdir(root):
        print(f"'{root}' is not a valid directory path.")
        return

    # List all the subdirectories in the root
    subdirs = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]
    
    for subdir in subdirs:
        print("processing : ", subdir)
        subdir_path = os.path.join(root, subdir)
        
        # Create the new directory (input_name) inside each subdirectory
        new_dir_path = os.path.join(subdir_path, input_name)
        os.makedirs(new_dir_path, exist_ok=True)

        # Move each item from the subdirectory to the new directory
        for item in os.listdir(subdir_path):
            item_path = os.path.join(subdir_path, item)
            
            # Make sure we're not moving the new directory itself
            if item != input_name:
                shutil.move(item_path, new_dir_path)

def run(root_path: str=None, new_folder_name: str=None):
    root_path = root_path or strip_quotes(input('Enter root folder path : '))
    new_folder_name = new_folder_name or strip_quotes(input("Enter new folder name to insert : "))
    move_subfolder_contents(root_path, new_folder_name)

if __name__ == "__main__":
    run()
