# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *
from _workplace.util.cut_video.cut_video import cut_time_by_time as cuttime
from _workplace.util.media_files_control import transfer_mp4_to_mp3 as trans

def new_label_sentence(label_file_path):
    lines = read_lines(label_file_path)
    new_lines = []
    new_start: str = None
    new_end: str = None
    new_text = None

    for i, line in enumerate(lines):
        starttime, endtime, text = line.split('\t')
        print(starttime, endtime, text)
        new_end = endtime
        text = text.strip()
        # if text.endswith('근데'):
        #     new_lines.append(new_start + '\t' + new_end + '\t' + new_text)
        #     new_start = starttime
        #     new_text = text
        #     new_end = endtime
        #     continue
        if text.endswith('세요') or text.endswith('니다') or text.endswith('시다') or text.endswith('어요') or text.endswith('에요') or text.endswith('죠') or text.endswith('거야') or text.endswith('잖아') or text.endswith('데요') or text.endswith('왔어') or text.endswith('이야') or text.endswith('을까') or text.endswith('텐데') or text.endswith('싶다') or text.endswith('이구나') or text.endswith('텐데') or text.endswith('구만') or text.endswith('없어') or text.endswith('아니야') or text.endswith('예요') or text.endswith('워요') or text.endswith('어떤가요') or text.endswith('텐데') or text.endswith('해요') or text.endswith('였다') or text.endswith('하고요') or text.endswith('해요') or text.endswith('었어') or text.endswith('봐요') or text.endswith('잖아요') or text.endswith('였구나') or text.endswith('더라') or text.endswith('었어') or text.endswith('있어') or text.endswith('그랬어') or text.endswith('거든요') or text.endswith('거든') or text.endswith('니요') or text.endswith('겠다') or text.endswith('했어') or text.endswith('않나') or text.endswith('않다') or text.endswith('았어') or text.endswith('해줘') or text.endswith('찮다') or text.endswith('잖니') or text.endswith('많아') or text.endswith('있나') or text.endswith('인가') or text.endswith('뺄까') or text.endswith('빼자') or text.endswith('빼요') or text.endswith('했네') or text.endswith('게요') or text.endswith('아요') or text.endswith('져요') or text.endswith('데요') or text.endswith('니까') or text.endswith('갈게') or text.endswith('어디가'):
            text += '.'
        if (text.endswith('.') or text.endswith('?') or text.endswith('!')):
            if new_text:
                new_text += ' ' + text
            else:
                new_text = text
                new_start = starttime
            print(f"new text : {new_text}")
            new_lines.append(new_start + '\t' + new_end + '\t' + new_text)
            new_start = None
            new_end = None
            new_text = None
        elif new_text:
            print(f"new : {new_text} text : {text}")
            new_text += ' ' + text
        else:
            new_start = starttime
            new_text = text
    return new_lines

def process_sentence(mp4_file_path, label_file_path):
    folder_path = parent_path(mp4_file_path)
    default_output_folder_path = create_folder(join_folder_path(folder_path, os.path.splitext(os.path.basename(mp4_file_path))[0]) + '_sentence')
    obj = cuttime(mp4_file_path)
    lines = new_label_sentence(label_file_path)
    print(lines)
    output_file_path = None
    for i, line in enumerate(lines):
        starttime, endtime, text = line.split('\t')
        print(starttime, endtime, text)
        text = text.strip().replace('?', '__').replace('.', '')
        output_file_name = '{}_{}_{}.mp4'.format(float(starttime).__floor__(), float(endtime).__round__(), text.replace('\n', '').replace('\n', ''))
        output_file_path = join_folder_path(default_output_folder_path, output_file_name)
        if path_exist(output_file_path):
            continue
        obj.cut_video_time_no_stamp(starttime, endtime, output_file_path)
        # trans.run('2', output_file_path)

def process(mp4_file_path, label_file_path):
    folder_path = parent_path(mp4_file_path)
    default_output_folder_path = create_folder(join_folder_path(folder_path, os.path.splitext(os.path.basename(mp4_file_path))[0]))
    obj = cuttime(mp4_file_path)
    lines = read_lines(label_file_path)

    for i, line in enumerate(lines):
        starttime, endtime, text = line.split('\t')
        text = text.strip().replace('?', '__').replace('.', '')
        output_file_name = '{}_{}_{}.mp4'.format(starttime, endtime, text.replace('\n', '').replace('\n', ''))
        output_file_path = join_folder_path(default_output_folder_path, output_file_name)
        if path_exist(output_file_path):
            continue
        obj.cut_video_time_no_stamp(float(starttime).__floor__(), float(endtime).__round__(), output_file_path)
        trans.run('2', output_file_path)
        

def run():
    print('1. folder\n2. file')
    select = str(strip_quotes(input("Enter select process : ")))
    if select == '1':
        folder_path = strip_quotes(input('Enter folder path: '))
        mp4_files = get_files_path_in_folder_via_ext(folder_path, 'mp4')
        for i, mp4_file in enumerate(mp4_files):
            label_file_path = change_extension(mp4_file, 'txt')
            process(mp4_file, label_file_path)
            
    elif select == '2':
        mp4_file_path = strip_quotes(input('Enter mp4 file path: '))
        label_file_path = strip_quotes(input('Enter txt(label) file path: '))
        process_sentence(mp4_file_path, label_file_path)

if __name__ == "__main__":
    run()