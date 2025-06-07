# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *
from _workplace.library.junLib_csv import *
from pydub import AudioSegment
from _workplace.Jun.cut_video.cut_video_via_label_personal import new_label_sentence

class cut_audio:
    def __init__(self, input_path) -> None:
        self.input_path = input_path

    def cut_audio(self, start_time, end_time, i=''):
        self.input_path
        parent = parent_path(self.input_path)
        base_name = os.path.splitext(os.path.basename(self.input_path))[0]
        audio = AudioSegment.from_file(self.input_path)

        # 시작 및 종료 시간 계산 (단위: 밀리초)
        start_ms = start_time * 1000
        end_ms = end_time * 1000

        # 오디오 파일 자르기
        cut_audio = audio[start_ms:end_ms]
        output_name = "{}_{}-{}_{}".format(base_name, str(i).zfill(4) if i else '0001', str(start_time).zfill(3), str(end_time).zfill(3))
        create_folder(join_folder_path(parent, base_name))
        output_path = join_folder_path(parent, base_name, output_name + '.mp3')

        # 오디오 파일 저장
        cut_audio.export(output_path, format="mp3")  # 원하는 형식으로 변경 가능
        return output_path

def process(input_file='', start=None, end=None):
    start = stqinput(start, 'start time')
    end = stqinput(end, 'end time')

    # 오디오 파일 자를 경로와 저장할 경로 설정
    input_file = ifinput(input_file, 'audio file')

    obj = cut_audio(input_file)
    start_time_stamp = start
    end_time_stamp = end
    # text = text.replace('\n', '').replace('\n', '').strip()

    # 오디오 파일 자르기
    output_file_path = obj.cut_audio(float(start_time_stamp), float(end_time_stamp))

def run():
    print('1. folder\n2. file')
    select = str(strip_quotes(input("Enter select process : ")))
    if select == '1':
        folder_path = strip_quotes(input('Enter folder path : '))
        extension = strip_quotes(input('Enter target extension(wav, mp3, etc.) : '))
        files = get_files_path_in_folder_via_ext(folder_path, extension)
        for i, file in enumerate(files):
            process(file)

    elif select == '2':
        file_path = strip_quotes(input('Enter audio file path: '))
        while(True):
            process(file_path)


if __name__ == "__main__":
    run()