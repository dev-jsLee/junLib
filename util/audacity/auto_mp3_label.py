# -*- coding: utf-8 -*-
import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.library.junLib import *
from _workplace.util.audacity.pipeclient import PipeClient
from _workplace.util.audacity.pipeclient_jun import PipeClient_jun
from _workplace.util.media_files_control import transfer_mp4_to_mp3 as transfer
import time  # time 모듈을 추가합니다.
from _workplace.util.audacity.save_label_txt import run as transfer_to_txt



ffmpeg_path = join_folder_path(root_folder_path, '_resource', 'ffmpeg-n5.1-latest-win64-lgpl-5.1', 'bin') + '\\ffmpeg'
def convert_audio(input_file, output_file=None, extension='wav', ffmpeg_path=ffmpeg_path, overwrite=None):
    output_file = output_file or rename(input_file, new_extension=extension)
    cmd = [
        ffmpeg_path,
        '-i', input_file,
        '-ar', '44100',
        '-ab', '192k',
        '-acodec', 'pcm_f32le',  # 32-비트 실수 코덱을 지정
        '-sample_fmt', 'flt',
        '-y',
        output_file
    ]
    if overwrite:
        cmd.append(overwrite)

    subprocess.run(cmd, check=True)
    return output_file

def get_track_info(client: PipeClient_jun):
    # Audacity에서 트랙 정보를 가져옵니다.
    client.write("GetInfo: Type=Tracks Format=JSON")
    
    # 응답을 받아옵니다.
    response = client.read()
    
    # 응답을 분석하여 필요한 정보를 추출합니다. (예: 파일 경로)
    # 이 부분은 Audacity의 응답 형식에 따라 파싱 코드를 작성해야 합니다.
    # LISP 형식의 응답을 파싱하는 코드를 추가해야 합니다.

    return response

def import_mp3_and_set_labels_from_input(client:PipeClient_jun, mp3_file_path=None, new_wav_file_path=None, convert=True):
    # 사용자로부터 mp3 파일 경로와 레이블 txt 파일 경로를 입력받습니다.
    # mp3_file_path = "E20200921_00002_048_01-143.520_150.200-neutral_aeng_keo_nam_02.mp3" or strip_quotes(input("Enter mp3 file path: "))
    mp3_file_path = mp3_file_path or strip_quotes(input("Enter mp3 file path: "))
    label_file_path = rename(mp3_file_path, new_extension='txt')
    
    # client.write(f'SetProject: Name="{os.path.splitext(os.path.basename(os.path.abspath(mp3_file_path)))[0]}"')
    client.set_project_name(os.path.splitext(os.path.basename(os.path.abspath(mp3_file_path)))[0])
    # mp3 파일을 Audacity에 가져옵니다.
    # new_wav_file_path = convert_audio(mp3_file_path, extension='mp3')
    print(os.path.splitext(os.path.basename(mp3_file_path))[1])
    # if os.path.splitext(os.path.basename(mp3_file_path))[1] != ".wav":
        # new_wav_file_path = convert_audio(mp3_file_path, extension='wav')
        # time.sleep(3)  # 오디오 파일을 가져온 후 약간의 지연 시간을 둡니다.
    # new_wav_file_path = new_wav_file_path or rename(mp3_file_path, suffix='_converted', new_extension='wav')
    # if convert:
        # convert_audio(mp3_file_path, new_wav_file_path, ffmpeg_path=ffmpeg_path, overwrite='-y')
    # copy_and_rename_file(mp3_file_path, new_wav_file_path)
    new_wav_file_path = str(os.path.abspath(mp3_file_path)).replace('\\', '/')
    client.write(f'Import2: Filename="{new_wav_file_path}"')
    time.sleep(1)  # 오디오 파일을 가져온 후 약간의 지연 시간을 둡니다.

    # 새로운 레이블 트랙을 생성합니다.
    client.write("NewLabelTrack")
    client.write("LastTrack")
    client.write(f"SetTrackStatus: Name={os.path.splitext(os.path.basename(os.path.abspath(mp3_file_path)))[0]}")

    # txt 파일에서 레이블 정보를 읽어옵니다.
    with open(label_file_path, 'r', encoding='utf-8') as txt_file:
        for i, line in enumerate(txt_file):
            # 여기서는 간단하게 각 줄을 레이블로 추가한다고 가정합니다.
            # 실제로는 txt 파일의 형식에 따라 파싱이 필요할 수 있습니다.
            if line.strip():
                start_time, end_time, text = line.strip().split("\t")
                print(start_time, "\t", end_time, "\t", text)
                client.write(f'SelectTime: End={end_time} Start={start_time}')
                client.write(f'AddLabel')
                client.write(f'SetLabel: End={end_time} Start={start_time} Text="{text}" Label="{i}')
    return client

def run(client:PipeClient_jun=PipeClient_jun(), mp3_file_path=None, new_wav_file_path=None, convert=False): # type:ignore
    client.delete_all()
    client = import_mp3_and_set_labels_from_input(client=client, mp3_file_path=mp3_file_path, new_wav_file_path=new_wav_file_path, convert=convert)
    input("Enter to continue")
    txt_file_path = rename(mp3_file_path, new_extension='txt')
    client.set_txt_file_path(txt_file_path)
    client.save_to_label()
    print(f"==========\nfolder: {os.path.dirname(txt_file_path)}\n==========")
    print(f"==========\n{os.path.basename(txt_file_path)}\n==========")
    input("Enter to continue after save label")
    clear()
    """
        저장 여부 검사 코드
    """
    
    print("레이블 파일을 올바른 위치에 저장했는지 검사합니다.")
    while(not path_exist(rename(mp3_file_path, new_extension='txt.bak'))):
        clear()
        print("저장이 되지 않았습니다.\n저장 후 진행 바랍니다.")
        print(f"==========\nfolder: {os.path.dirname(txt_file_path)}\n==========")
        print(f"==========\n{os.path.basename(txt_file_path)}\n==========")
        input("Enter to continue after save label")
    """
        빈 레이블 검사 코드
    """
    print("빈 레이블이 있는지 검사합니다.")
    need_to_check_empty_text = True
    while(need_to_check_empty_text):
        while_break_flag = True
        lines = read_lines(txt_file_path)
        target = 0
        for i, line in enumerate(lines, 1):
            if line.strip().__contains__('\t'):
                start, end, text = line.split('\t')
                if not text.strip():
                    while_break_flag = False
                    target = i
                    break
        if while_break_flag: break
        else:
            print(f"레이블 중 {target}번째 줄에 빈 레이블이 있습니다. 레이블/텍스트 파일 수정 및 저장 후 진행 바랍니다.")
            input("Enter to continue")
    print("빈 레이블 없음. 통과.")

    client.delete_all()
    return client

if __name__ == "__main__":
    # 사용 예제
    # client = PipeClient()
    # import_mp3_and_set_labels_from_input(client)
    # print(get_track_info(client))
    run()