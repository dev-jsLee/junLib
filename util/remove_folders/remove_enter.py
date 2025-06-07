# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *

def process(txt_file):
    lines = read_lines(txt_file)
    print(lines[0])
    print(lines[1])
    print(lines[2])

    new_lines = []
    for line in lines:
        new_line = line.strip()
        print(new_line)
        new_lines.append(new_line)
    write_to_file(txt_file, new_lines)
def process_(txt_file):
    import json

    with open(txt_file, 'r', encoding='utf-8') as file:
        content = file.read().replace('\n', '')

    # output = {'content': content}
    content_list = []
    content_list.append(content)
    write_to_file(txt_file, content_list)
def run():
    txt_file = strip_quotes(input('Enter txt file : '))
    process_(txt_file)
    pass

if __name__ == "__main__":
    run()