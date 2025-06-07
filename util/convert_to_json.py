# -*- coding: utf-8 -*-
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *

def process():
    pass

def run():
    input_file = strip_quotes(input('Enter txt file: '))
    output_file = change_extension(input_file, 'json')
    # process()
    convert_to_pretty_json(input_file, output_file)
    pass


def convert_to_pretty_json(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    json_data = json.loads(content)

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    run()


