# total_length_parent_folder.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from _workplace.library.junLib import *

def read_text_files(folder):
    face_speak_times = {'seconds': 0, 'minutes': 0}
    speech_times = {'seconds': 0, 'minutes': 0}
    actual_times = {'seconds': 0, 'minutes': 0}

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith("_total.txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip()
                        data = line.split('\t')
                        category = data[0]
                        seconds = float(data[1])
                        minutes = float(data[2])
                        if category == 'face_speak':
                            face_speak_times['seconds'] += seconds
                            face_speak_times['minutes'] += minutes
                        elif category == 'speech':
                            speech_times['seconds'] += seconds
                            speech_times['minutes'] += minutes
                        elif category == 'actual_total':
                            actual_times['seconds'] += seconds
                            actual_times['minutes'] += minutes

    return face_speak_times, speech_times, actual_times

def write_to_text_file(folder_path, face_speak_times, speech_times, actual_times):
    output_file_path = os.path.join(folder_path, "__total_.txt")
    with open(output_file_path, "w", encoding='utf-8') as f:
        face = f"face_speak_times: {cut_after_dot(str(face_speak_times['seconds']), length_after_dot=2)}, {cut_after_dot(str(float(face_speak_times['seconds'])/60),length_after_dot=2)}min\n"
        print(face)
        f.write(face)
        f.write(f"speech_times: {cut_after_dot(str(speech_times['seconds']), length_after_dot=2)}s, {cut_after_dot(str(speech_times['minutes']),length_after_dot=2)}min\n")
        f.write(f"actual_total : {cut_after_dot(str(actual_times['seconds']), length_after_dot=2)}s, {cut_after_dot(str(actual_times['minutes']),length_after_dot=2)}min")
    return output_file_path

def run(folder_path):
    if not folder_path:
        folder_path = input("폴더 경로를 입력하세요: ")
    folder_path = strip_quotes(folder_path)
    face_speak_times, speech_times, actual_times = read_text_files(folder_path)
    last_output_file = write_to_text_file(folder_path, face_speak_times, speech_times, actual_times)
    print(f"텍스트 파일 {last_output_file}이 성공적으로 출력되었습니다.")
    return last_output_file

if __name__ == "__main__":
    run()
