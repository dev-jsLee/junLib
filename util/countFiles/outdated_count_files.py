import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from _workplace.library.junLib import *

def count_files(folder_path, file_extension=None):
    folder_path = strip_quotes(folder_path)
    file_count = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file_extension is None or file.endswith(file_extension):
                file_count += 1
    return file_count

def run():
    folder_paths = []
    while True:
        folder_path = input("Enter folder path (press Enter to finish): ")
        if not folder_path:
            break
        folder_paths.append(strip_quotes(folder_path))
    if not folder_paths:
        print("No folder paths provided.")
        return

    file_counts = []
    for folder_path in folder_paths:
        total_files = count_files(folder_path)
        file_counts.append(total_files)
        print(f"Total number of files in {folder_path}: {total_files}")
    print("Total files count:", sum(file_counts))

if __name__ == "__main__":
    run()
