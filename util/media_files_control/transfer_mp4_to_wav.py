# -*- coding: utf-8 -*-
import subprocess
from tqdm import tqdm
import os
import sys
from __init__ import *
sys.path.append(source_code_path)
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *

ffmpeg_path = join_folder_path(root_folder_path, '_resource', 'ffmpeg-n5.1-latest-win64-lgpl-5.1', 'bin') + '\\ffmpeg'
print(ffmpeg_path)
def convert_audio(input_file, output_file=None, extension='wav',ffmpeg_path=ffmpeg_path):
    output_file = output_file or rename(input_file, new_extension=extension)
    cmd = [
        ffmpeg_path,
        '-i', input_file,
        # '-ar', '44100',
        '-ar', '16000',
        '-ab', '192k',
        output_file,
        '-y'
    ]

    subprocess.run(cmd, check=True)
    return output_file

def process_file(wav_file=None, toExtension='mp3', ffmpeg_path:str=ffmpeg_path):
    wav_file = strip_quotes(input('Enter target file: ')) if not wav_file else wav_file
    refined_media_file = change_extension(wav_file, toExtension)
    print(refined_media_file)
    if wav_file[-3:] != toExtension and not path_exist(refined_media_file):
        # subprocess.call(['ffmpeg', '-i', path, 'audio.wav', '-y'])
        # subprocess.call([ffmpeg_path, '-i', wav_file, rename(wav_file, new_extension=toExtension), '-y'])
        convert_audio(wav_file, extension=toExtension, ffmpeg_path=ffmpeg_path)
        print(f'Make {refined_media_file}')
    return refined_media_file

def run(select=None, target_path='', fromExtension='mp4', toExtension='mp3', ffmpeg_path=ffmpeg_path):
    """
    select : 'folder' or 'file'
    'folder' is '1' or 'folder'
    'file' is '2' or 'file'
    """
    if not select:
        print('1. folder\n2. file') 
    select = str(strip_quotes(input('select num : '))) if not select else select
    result = []
    if select == '1' or select == 'folder':
        # data 폴더 바로 아래의 .mp4 파일을 모두 찾습니다.
        target_path = strip_quotes(input('Enter folder path : ')) if not target_path else target_path
        mp4_files = get_files_path_in_folder_via_ext(target_path, fromExtension)
        # mp4_files = get_files_path_in_folder_via_ext(target_path, 'mp4')
        # mp4_files = f'{target_path}/*.{ext}'
        # wav_files = glob.glob(mp4_files)
        # tqdm을 사용하여 진행 상황을 보여줍니다.
        # for wav_file in tqdm(wav_files, desc="Processing audio files"):
        # print(wav_file)
        for i, wav_file in enumerate(mp4_files):
            result.append(process_file(wav_file, toExtension, ffmpeg_path=ffmpeg_path))
    elif select == '2' or select == 'file':
        target_path = target_path or strip_quotes(input('Enter file path : '))
        result.append(process_file(target_path, toExtension, ffmpeg_path=ffmpeg_path))
    elif select == '3':
        target_path = target_path or strip_quotes(input('Enter folder path : '))
        toExtension = strip_quotes(input("Enter to extension : "))
        speaker_folders = get_dir_sub_folder_path(target_path)
        for idx, speaker_folder_path in enumerate(speaker_folders):
            mp4_files = get_files_path_in_folder_via_ext(speaker_folder_path, fromExtension)
            for i, wav_file in enumerate(mp4_files):
                result.append(process_file(wav_file, toExtension, ffmpeg_path=ffmpeg_path))
    return result

if __name__ == "__main__":
    ext = strip_quotes(input('Enter extension. enter empty "mp4" : '))
    if not ext:
        ext = 'mp4'
    run(fromExtension=ext, toExtension='wav')