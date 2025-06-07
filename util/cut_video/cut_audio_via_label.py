# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *
from _workplace.library.junLib_csv import *
from pydub import AudioSegment
from _workplace.Jun.cut_video.cut_video_via_label_personal import new_label_sentence
from _workplace.Jun.cut_video.rename_vocal_files import *

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
        output_name = "{}_{}".format(base_name, str(i).zfill(4) if i else '0001')
        create_folder(join_folder_path(parent, base_name))
        output_path = join_folder_path(parent, base_name, output_name + '.mp3')

        # 오디오 파일 저장
        cut_audio.export(output_path, format="mp3")  # 원하는 형식으로 변경 가능
        return output_path

def process2(source_file_path):
    parent = parent_path(source_file_path)
    base_name = os.path.splitext(os.path.basename(source_file_path))[0]
    target_folder_path = join_folder_path(parent, base_name)
    pass

def process(input_file='', label_file=''):

    # 오디오 파일 자를 경로와 저장할 경로 설정
    input_file = ifinput(input_file, 'audio file')
    label_file = label_file if label_file else rename(input_file, suffix='-label', new_extension='txt')
    new_lines = new_label_sentence(label_file)
    print(new_lines)
    new_label_file = write_to_file(rename(label_file, suffix='-refined', new_extension='txt'), new_lines)
    input()
    # new_label_file = add_columns_and_vaules_for_csv(new_label_file, col_names=['start', 'end', 'text'])
    obj = cut_audio(input_file)
    new_lines = read_lines(new_label_file)
    files_path_list = []
    label_lines_for_csv = []
    label_lines_for_csv.append('index\tstart\tend\ttext\tfilename')
    for i, line in enumerate(new_lines, 1):
        start_time_stamp, end_time_stamp, text = line.split('\t')
        text = text.replace('\n', '').replace('\n', '').strip()
        # 오디오 파일 자르기
        output_file_path = obj.cut_audio(float(start_time_stamp), float(end_time_stamp), i)
        files_path_list.append(output_file_path)
        output_file_basename = os.path.basename(output_file_path)
        # result_file_basename = output_file_basename.split('-')[0]
        result_file_basename = output_file_basename
        text_line = f"{str(i).zfill(3)}\t{start_time_stamp}\t{end_time_stamp}\t{text}\t{result_file_basename}"
        label_lines_for_csv.append(text_line)
    label_file_for_csv = write_to_file(rename(label_file, suffix='-csv'), label_lines_for_csv)
    # new_label_file = add_files_name_for_csv(new_label_file, files_path_list)
    csv_file = convert_text_to_csv(label_file_for_csv)
    convert_csv_to_txt(csv_file)
    move_file_to_current_other_folder(label_file)
    move_file_to_current_other_folder(label_file_for_csv)

    process2(input_file)

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
        process(file_path)


if __name__ == "__main__":
    run()