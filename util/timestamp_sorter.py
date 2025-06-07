# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *

def process(file_path='', time_to_minus: float=0):
    lines = read_lines(file_path)
    new_lines = []
    for i, line in enumerate(lines):
        start, end, text = str(line).split('\t')
        new_start = float(start)-float(time_to_minus)
        if new_start < 0:
            new_start = 0
        new_end = float(end)-float(time_to_minus)
        new_line = "{:.2f}\t{:.2f}\t{}".format(new_start, new_end, text.replace('\n', ''))
        new_lines.append(new_line)
    write_to_file(rename(file_path, suffix='-refined'), new_lines)

def run(file_path=''):
    file_path = stqinput(file_path, 'txt file path')
    time_to_minus = float(strip_quotes(input('Enter sec : ')))
    process(file_path, time_to_minus)

if __name__ == "__main__":
    run()