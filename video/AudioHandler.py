"""
오디오 파일 처리를 위한 핸들러 클래스
"""
import os
import sys
import subprocess
import json
import time
from .. import junLib
from . import junLib_csv
from . import junLib_xml
from . import junLib_xml_class
from . import junLib_xml_class_json

# PyQt5 임포트
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget, QComboBox, QLabel, QLineEdit, QTextEdit, QHBoxLayout, QRadioButton, QButtonGroup
from PyQt5.QtCore import QTimer

# ffmpeg 경로 설정
ffmpeg_folder_path = os.path.join(os.path.dirname(__file__), '_resource', 'ffmpeg-n5.1-latest-win64-lgpl-5.1', 'bin')
ffplay_path = os.path.join(ffmpeg_folder_path, 'ffplay')
ffmpeg_path = os.path.join(ffmpeg_folder_path, 'ffmpeg')

# 감정 태그 정의
EMOTION_TAGS = {
    '01': {
        'kor': '평범',
        'eng': 'neutral',
        'code': 1
    },
    '02': {
        'kor': '놀람',
        'eng': 'surprise',
        'code': 2
    },
    '03': {
        'kor': '슬픔',
        'eng': 'sadness',
        'code': 3
    },
    '04': {
        'kor': '행복함',
        'eng': 'happiness',
        'code': 4
    },
    '05': {
        'kor': '두려움',
        'eng': 'fear',
        'code': 5
    },
    '06': {
        'kor': '역겨움',
        'eng': 'disgust',
        'code': 6
    },
    '07': {
        'kor': '화남',
        'eng': 'angry',
        'code': 7
    }
}

class AudioHandler:
    """오디오 파일을 처리하기 위한 핸들러 클래스"""
    
    def __init__(self, audio_path='') -> None:
        """
        AudioHandler 초기화
        
        Args:
            audio_path (str, optional): 오디오 파일 경로. 기본값은 빈 문자열.
        """
        if audio_path:
            self.set_audio(audio_path)

    def set_audio(self, audio_path=''):
        """
        오디오 파일 경로 설정
        
        Args:
            audio_path (str, optional): 오디오 파일 경로. 기본값은 빈 문자열.
            
        Returns:
            AudioHandler: 체이닝을 위한 self 반환
        """
        self.audio_path = audio_path or junLib.strip_quotes(input("Enter audio file path : "))
        return self

    def get_duration(self):
        """
        오디오 파일의 재생 시간을 초 단위로 반환
        
        Returns:
            float: 오디오 재생 시간(초)
        """
        clip = AudioFileClip(self.audio_path)
        self.duration = float(clip.duration)
        clip.close()
        return self.duration

class EmotionTaggingApp(QMainWindow):
    """감정 태깅을 위한 GUI 애플리케이션"""
    
    def __init__(self, worker_code, yymmdd_folder_path=None):
        """
        EmotionTaggingApp 초기화
        
        Args:
            worker_code (str): 작업자 코드
            yymmdd_folder_path (str, optional): 작업할 폴더 경로. 기본값은 None.
        """
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

        self.btnSave = QPushButton("Save Emotion Data", self)
        self.btnSave.clicked.connect(self.saveEmotionData)

        layout = QVBoxLayout()
        layout.addWidget(self.btnOpenFolder)

        workerLayout = QHBoxLayout()
        layout.addLayout(workerLayout)
        
        self.btnPlayVideo = QPushButton("Play Video", self)
        self.btnPlayVideo.clicked.connect(self.play_current_video)
        layout.addWidget(self.btnPlayVideo)

        self.emotionRadioButtons = {}
        self.emotionButtonGroup = QButtonGroup(self)
        for code, emotion_info in EMOTION_TAGS.items():
            radioButton = QRadioButton(emotion_info['eng'], self)
            self.emotionRadioButtons[emotion_info['eng']] = radioButton
            self.emotionButtonGroup.addButton(radioButton)
            layout.addWidget(radioButton)

        layout.addWidget(self.btnSave)

        container = QWidget(self)
        container.setLayout(layout)

        self.setCentralWidget(container)
        if self.yymmdd_folder_path:
            QTimer.singleShot(0, lambda: self.openFolder(self.yymmdd_folder_path))

    def openFolder(self, yymmdd_folder_path=None):
        """
        작업할 폴더를 엽니다.
        
        Args:
            yymmdd_folder_path (str, optional): 폴더 경로. 기본값은 None.
        """
        self.yymmdd_folder_path = yymmdd_folder_path or QFileDialog.getExistingDirectory(self, "Open yymmdd Folder")

        self.target_remain_video_list = []
        self.at_all_list = []
        if self.yymmdd_folder_path:
            emotion_folder = os.path.join(self.yymmdd_folder_path, 'emotion')
            speaker_folders = junLib.get_sub_folder_path(emotion_folder)
            for i, speaker_folder in enumerate(speaker_folders, 1):
                files = junLib.get_files_path_in_folder_via_ext(speaker_folder, 'mp4')
                for j, video_path in enumerate(files, 1):
                    current_xml_file = junLib.rename(video_path, new_extension='xml')
                    self.at_all_list.append(video_path)
                    if self.this_worker_did_this_file(current_xml_file):
                        continue
                    self.target_remain_video_list.append(video_path)
        self.file_total_count = len(self.target_remain_video_list)
        self.play_next_video()

    def play_current_video(self):
        """현재 비디오를 재생합니다."""
        if self.process and self.process.poll() is not None:
            self.process = subprocess.Popen([ffplay_path, self.video_path])
            
    def play_next_video(self):
        """다음 비디오를 재생합니다."""
        self.process.terminate() if self.process else None
        subprocess.run(['cmd', '/c', 'cls'])
        if self.target_remain_video_list:
            self.video_path = self.target_remain_video_list.pop(0)
            xml_file_path = os.path.abspath(junLib.rename(self.video_path, new_extension='xml'))
            print(f"{str(len(self.at_all_list)).zfill(3)}/{str(int(len(self.at_all_list) - len(self.target_remain_video_list))).zfill(3)}")
            print(self.video_path)
            print(os.path.basename(self.video_path))
            
            self.setWindowTitle(f"Emotion Tagging App : {os.path.basename(os.path.dirname(self.video_path))}/{os.path.basename(self.video_path)}")
            
            self.process = subprocess.Popen([ffplay_path, self.video_path])
            self.current_xml_file = xml_file_path
        else:
            print("All videos have been processed!")

    def saveEmotionData(self):
        """선택된 감정 데이터를 저장합니다."""
        if not self.current_xml_file:
            subprocess.run(['cmd', '/c', 'cls'])
            print("No Opened folder.")
            return

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

        if hasattr(self, 'current_xml_file') and self.current_xml_file:
            emotion_data = {
                '__text__': emotion,
                'code': current_index,
                'eng': emotion,
                'kor': EMOTION_TAGS[current_index]['kor'],
                'worker': self.worker_code,
                'priority': priority
            }
        junLib.process_xml(self.current_xml_file, emotion_data)
        print(f"{os.path.basename(self.video_path)} : {emotion} saved!")
        print(len(self.this_worker_did_this_file(self.current_xml_file)))
        if len(self.this_worker_did_this_file(self.current_xml_file)) < 2:
            pass
        else:
            self.process.terminate()
            self.play_next_video()

    def this_worker_did_this_file(self, xml_file_path):
        """
        현재 작업자가 해당 파일을 처리했는지 확인합니다.
        
        Args:
            xml_file_path (str): XML 파일 경로
            
        Returns:
            list: 작업자 코드 목록
        """
        worker_codes = junLib.search_xml_by_attribute(xml_file_path, 'emotion', 'worker', self.worker_code)
        return worker_codes

def process_xml(xml_file_path, emotion_data):
    # converter = JsonToXmlConverter(emotion_data)
    obj = junLib_xml.XmlToJsonConverter(xml_file_path)
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
    obj = junLib_xml_class_json.JsonToXmlConverter(json_data, 'annotation')
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
        worker_code = junLib.strip_quotes(input('Enter your worker code(ex 4) : '))
        if not worker_code in num_list:
            continue
        yymmdd_folder_path = junLib.strip_quotes(input('Enter yymmdd folder path(option): '))
        app = QApplication(sys.argv)
        window = EmotionTaggingApp(yymmdd_folder_path, worker_code)
        window.show()
        sys.exit(app.exec_())
