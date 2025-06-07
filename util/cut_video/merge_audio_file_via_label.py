# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *
from _workplace.Jun.cut_video.cut_audio import cut_audio as cut_audio

def process(source_file_path, first_audio, second_audio):
    first_file_base_name = os.path.splitext(os.path.basename(first_audio))[0]
    second_file_base_name = os.path.splitext(os.path.basename(second_audio))[0]
    i = first_file_base_name.split('-')[0].split('_')[-1]
    start_time = first_file_base_name.split('-')[-1].split('_')[0]
    end_time = second_file_base_name.split('-')[-1].split('_')[1]
    obj = cut_audio(source_file_path)
    obj.cut_audio(float(start_time), float(end_time), i)

def run():
    source_file_path = stqinput('', 'source file path')
    first_audio = stqinput('', 'first audio file path')
    second_audio = stqinput('', 'second audio file path')
    process(source_file_path, first_audio, second_audio)

if __name__ == "__main__":
    run()