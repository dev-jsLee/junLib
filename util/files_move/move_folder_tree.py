import os
import shutil
from __init__ import *
from _workplace.library.junLib import *

# def move_folder_structure(src_path: str, dest_path: str):
#     """
#     원본 폴더의 파일 및 폴더 구조를 그대로 도착지 폴더로 이동합니다.

#     :param src_path: 원본 폴더 경로
#     :param dest_path: 도착지 폴더 경로
#     """
#     # 원본 폴더의 이름을 가져옵니다.
#     src_folder_name = os.path.basename(src_path)
#     # 도착지 폴더 내에 원본 폴더와 동일한 이름의 폴더 경로를 생성합니다.
#     final_dest_path = os.path.join(dest_path, src_folder_name)

#     # 원본 폴더를 도착지 폴더로 이동합니다.
#     shutil.move(src_path, final_dest_path)
#     print(f"'{src_path}'를 '{final_dest_path}'로 이동했습니다.")

def move_sentence_family_folder_and_files(speaker_folder_path=None, index:int=0, total:int=0):
    speaker_folder_path = speaker_folder_path or strip_quotes(input('Enter folder path : '))
    sentece_folders = get_dir_sub_folder_path(speaker_folder_path)
    mp4_files = get_files_path_in_folder_via_ext(speaker_folder_path, 'mp4')
    for i, mp4_file_path in enumerate(mp4_files, 1):
        family_file_name = os.path.splitext(os.path.basename(mp4_file_path))[0]
        # length = len(list(family_file_name))
        family_files = get_files_path_in_folder_via_startwith(speaker_folder_path, family_file_name)
        Eyyyymmdd = str(family_file_name).split('_')[0]
        for j, family_file_path in enumerate(family_files, 1):
            clear()
            if index!=0 and total!=0: print(f"{index}/{total}\tspeaker")
            print(f"{i}/{len(mp4_files)}\n{j}/{len(family_files)}")
            move_file_to_current_other_folder(family_file_path, Eyyyymmdd, show_msg=False)
        # sentence_img_folder_path = join_folder_path(speaker_folder_path, str(os.path.splitext(os.path.basename(mp4_file_path))[0]))
        # move_folder_structure(sentence_img_folder_path, join_folder_path(speaker_folder_path, Eyyyymmdd), True)
    # for i, file_path in enumerate(files):
    #     length = len(list(str(os.path.basename(file_path)).split('_')[0]))
    #     move_file_to_subfolders(file_path=file_path, match_length=length)
    # for i, sentence_folder_path in enumerate(sentece_folders, 1):
    #     Eyyyymmdd = str(os.path.basename(sentence_folder_path)).split('_')[0]
    #     move_folder_structure(sentence_folder_path, join_folder_path(speaker_folder_path, Eyyyymmdd))

def run(speaker_root_folder_path=None):
    speaker_root_folder_path = speaker_root_folder_path or strip_quotes(input("Enter speaker root folder path : "))
    speakers = get_dir_sub_folder_path(speaker_root_folder_path)
    for i, speaker_folder_path in enumerate(speakers, 1):
        move_sentence_family_folder_and_files(speaker_folder_path=speaker_folder_path, index=i, total=len(speakers))

if __name__ == "__main__":
    run()

    # move_sentence_family_folder_and_files()

    # src_path = input("원본 폴더 경로를 입력하세요: ")
    # dest_path = input("도착지 폴더 경로를 입력하세요: ")
    # move_folder_structure(src_path, dest_path)
