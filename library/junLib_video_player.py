import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.library.junLib import *
from _workplace.library.junLib_importlib import auto_import
auto_import('PyQt5', 'pyqt5')
from _workplace.library.junLib_csv import *
from _workplace.library.junLib_xml import *
from _workplace.library.junLib_xml_class import *
from _workplace.library.junLib_xml_class_json import *
import subprocess
import json
import time
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget, QComboBox, QLabel, QLineEdit, QTextEdit, QHBoxLayout, QRadioButton, QButtonGroup
from PyQt5.QtCore import QTimer

ffmpeg_folder_path = join_folder_path(root_folder_path, '_resource', 'ffmpeg-n5.1-latest-win64-lgpl-5.1', 'bin')
ffplay_path = join_folder_path(ffmpeg_folder_path, 'ffplay')
ffmpeg_path = join_folder_path(ffmpeg_folder_path, 'ffmpeg')
emt = {
    '01':{
        'kor':'평범',
        'eng':'neutral',
        'code': 1
    },
    '02':{
        'kor':'놀람',
        'eng':'surprise',
        'code': 2
    },
    '03':{
        'kor':'슬픔',
        'eng':'sadness',
        'code': 3
    },
    '04':{
        'kor':'행복함',
        'eng':'happiness',
        'code': 4
    },
    '05':{
        'kor':'두려움',
        'eng':'fear',
        'code': 5
    },
    '06':{
        'kor':'역겨움',
        'eng':'disgust',
        'code': 6
    },
    '07':{
        'kor':'화남',
        'eng':'angry',
        'code': 7
    }
}

class EmotionTaggingApp(QMainWindow):
    def __init__(self, worker_code, yymmdd_folder_path=None):
        super().__init__()
        self.file_total_count = None
        self.at_all_list = None
        self.video_path = None
        self.process = None
        self.current_xml_file = None
        self.worker_code = str(worker_code).zfill(3)
        self.yymmdd_folder_path = yymmdd_folder_path if os.path.isdir(yymmdd_folder_path) else None
        
        self.setWindowTitle("Emotion Tagging App")
        self.setGeometry(100, 100, 600, 400)

        self.btnOpenFolder = QPushButton("Open _merging/yymmdd Folder", self)
        self.btnOpenFolder.clicked.connect(self.openFolder)

        # self.emotionLabel = QLabel("Emotion:", self)
        # self.emotionComboBox = QComboBox(self)
        # self.emotionComboBox.addItems(["neutral", "surprise", "sadness", "happiness", "fear", "disgust", "angry"])
        # 감정 라디오 버튼 생성
        # self.commentLabel = QLabel("Comments:", self)
        # self.commentTextEdit = QTextEdit(self)

        self.btnSave = QPushButton("Save Emotion Data", self)
        self.btnSave.clicked.connect(self.saveEmotionData)

        layout = QVBoxLayout()
        layout.addWidget(self.btnOpenFolder)

        workerLayout = QHBoxLayout()
        layout.addLayout(workerLayout)
        
        # 영상 재생 버튼 추가
        self.btnPlayVideo = QPushButton("Play Video", self)
        self.btnPlayVideo.clicked.connect(self.play_current_video)
        layout.addWidget(self.btnPlayVideo)

        self.emotionRadioButtons = {}
        self.emotionButtonGroup = QButtonGroup(self)
        for code, emotion_info in emt.items():
            radioButton = QRadioButton(emotion_info['eng'], self)
            self.emotionRadioButtons[emotion_info['eng']] = radioButton
            self.emotionButtonGroup.addButton(radioButton)
            layout.addWidget(radioButton)
        # emotionLayout = QHBoxLayout()
        # emotionLayout.addWidget(self.emotionLabel)
        # emotionLayout.addWidget(self.emotionComboBox)
        # layout.addLayout(emotionLayout)

        # layout.addWidget(self.commentLabel)
        # layout.addWidget(self.commentTextEdit)
        layout.addWidget(self.btnSave)

        container = QWidget(self)
        container.setLayout(layout)

        self.setCentralWidget(container)
        if self.yymmdd_folder_path:
            QTimer.singleShot(0, lambda: self.openFolder(self.yymmdd_folder_path))

    def openFolder(self, yymmdd_folder_path=None):
        self.yymmdd_folder_path = yymmdd_folder_path or QFileDialog.getExistingDirectory(self, "Open yymmdd Folder")

        self.target_remain_video_list = []
        self.at_all_list = []
        if self.yymmdd_folder_path:
            emotion_folder = join_folder_path(self.yymmdd_folder_path, 'emotion')
            speaker_folders = get_sub_folder_path(emotion_folder)
            for i, speaker_folder in enumerate(speaker_folders, 1):
                files = get_files_path_in_folder_via_ext(speaker_folder, 'mp4')
                for j, video_path in enumerate(files, 1):
                    current_xml_file = rename(video_path, new_extension='xml')
                    self.at_all_list.append(video_path)
                    if self.this_worker_did_this_file(current_xml_file):
                        continue
                    self.target_remain_video_list.append(video_path)
        self.file_total_count = len(self.target_remain_video_list)
        self.play_next_video()

    def play_current_video(self):
        if self.process and self.process.poll() is not None:  # process가 종료된 상태라면
            self.process = subprocess.Popen(["ffplay", self.video_path])
            
    def play_next_video(self):
        self.process.terminate() if self.process else None
        subprocess.run(['cmd', '/c', 'cls'])
        if self.target_remain_video_list:
            self.video_path = self.target_remain_video_list.pop(0)
            xml_file_path = os.path.abspath(rename(self.video_path, new_extension='xml'))
            print(f"{str(len(self.at_all_list)).zfill(3)}/{str(int(len(self.at_all_list) - len(self.target_remain_video_list))).zfill(3)}")
            print(self.video_path)
            print(os.path.basename(self.video_path))
            
            # Set the window title to the video path
            self.setWindowTitle(f"Emotion Tagging App : {os.path.basename(os.path.dirname(self.video_path))}/{os.path.basename(self.video_path)}")
            
            self.process = subprocess.Popen(["ffplay", self.video_path])
            self.current_xml_file = xml_file_path
        else:
            print("All videos have been processed!")

    def saveEmotionData(self):
        if not self.current_xml_file:
            subprocess.run(['cmd', '/c', 'cls'])
            print("No Opened folder.")
            return
        # 선택된 라디오 버튼의 텍스트를 가져옴
        emotion = None
        current_index = 0
        for i, radioButton in enumerate(self.emotionRadioButtons.values(), 1):
            if radioButton.isChecked():
                emotion = radioButton.text()
                current_index = str(i).zfill(2)
                break
        if not emotion:
            subprocess.run(['cmd', '/c', 'cls'])
            print('No selected Emotion radio button.')
            return
        priority = str(len(self.this_worker_did_this_file(self.current_xml_file)) + 1)

        # XML 파일에 워커와 감정 정보를 추가하는 코드
        if hasattr(self, 'current_xml_file') and self.current_xml_file:
            emotion_data = {
                '__text__': emotion,
                'code': current_index,
                'eng': emotion,
                'kor': emt[current_index]['kor'],
                'worker': self.worker_code,
                'priority': priority
            }
        process_xml(self.current_xml_file, emotion_data)
        print(f"{os.path.basename(self.video_path)} : {emotion} saved!")
        print(len(self.this_worker_did_this_file(self.current_xml_file)))
        if len(self.this_worker_did_this_file(self.current_xml_file)) < 2:
            pass
        else:
            self.process.terminate()
            self.play_next_video()

    def this_worker_did_this_file(self, xml_file_path):
        worker_codes = search_xml_by_attribute(xml_file_path, 'emotion', 'worker', self.worker_code)
        return worker_codes
        # if worker_codes:
        #     return True
        # else:
        #     return False

def process_xml(xml_file_path, emotion_data):
    # converter = JsonToXmlConverter(emotion_data)
    obj = XmlToJsonConverter(xml_file_path)
    json_data = obj.convert_to_json()
    emotions = []
    if 'emotions' in json_data:
        if 'emotion' in json_data['emotions']:
            # print("json_data['emotions']['emotion'] ", json_data['emotions']['emotion'])
            if isinstance(json_data['emotions']['emotion'], dict):
                emotions.append(json_data['emotions']['emotion'])
            elif isinstance(json_data['emotions']['emotion'], list):
                for i, d in enumerate(json_data['emotions']['emotion']):
                    emotions.append(d)
        else:
            json_data['emotions']['emotion'] = []

    else:
        json_data['emotions'] = {}
        json_data['emotions']['emotion'] = []
    # print(emotion_data)
    emotions.append(emotion_data)
    json_data['emotions']['emotion'] = emotions
    obj = JsonToXmlConverter(json_data, 'annotation')
    obj.save_to_xml_file(xml_file_path)

if __name__ == "__main__":
    worker = ['이준상', '배권표','김동율','김성완','박가인','이수현']
    texts = ''
    num_list = []
    for i, name in enumerate(worker, 1):
        text = f"{str(i).zfill(3)}. {name}\n"
        texts += text
        num_list.append(str(i))
    print(texts)
    while(True):
        worker_code = strip_quotes(input('Enter your worker code(ex 4) : '))
        if not worker_code in num_list:
            continue
        yymmdd_folder_path = strip_quotes(input('Enter yymmdd folder path(option): '))
        app = QApplication(sys.argv)
        window = EmotionTaggingApp(yymmdd_folder_path, worker_code)
        window.show()
        sys.exit(app.exec_())
