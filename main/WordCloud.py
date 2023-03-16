from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer, QThread, Signal
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, 
    QPlainTextEdit, QFileDialog, QMessageBox, 
    QLabel, QDialog, QVBoxLayout, QTextEdit
)
import json
import os
from util.Converter import JsonToTxtConverter
json2text = JsonToTxtConverter()
import subprocess 
from WordCloudMaster import create_word_cloud as CWC
from WorldCloud_ui import Ui_Dialog
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

class WorkerThread(QThread):
    generate_finished = Signal(str)

    def __init__(self, json_path, image_path):
        super().__init__()
        self.json_path = json_path
        self.image_path = image_path

    def run(self):
        txt_path = json2text.convert_to_txt_file(self.json_path)
        print(txt_path, self.image_path)
        cloud_image_path = CWC.create_wordscloud(txt_path, self.image_path)
        print('路径: ', txt_path, self.image_path, cloud_image_path, sep='\n')
        # bat_file_path = os.path.join(os.path.dirname(self.json_path), "generateWordCloud.bat")
        # subprocess.run([bat_file_path])
        self.generate_finished.emit(cloud_image_path)

class ImageJsonGenerator(Ui_Dialog,QDialog):
    def __init__(self):
        super().__init__()
        self.WordCloudimage_path = os.path.join(PROJECT_DIR, f'wordcloud-master\love_test.png')
        self.setupUi(self)

        # 界面样式
        self.wordCloudQss()


        # 连接按钮的信号和槽函数
        self.btn_choose_json.clicked.connect(self.chooseJson)
        self.btn_choose_image.clicked.connect(self.chooseImage)
        self.btn_generate.clicked.connect(self.startGenerate)

        # 初始化变量
        self.json_path = None
        self.image_path = None
        self.is_generating = False

    def chooseJson(self):
        # 使用Qt自带的文件选择框而不是操作系统的原生文件选择框
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "选择JSON文件", "",
                                                   "JSON Files (*.json)", options=options)
        if file_name:
            self.json_path = file_name

    def chooseImage(self):
        # 弹出文件选择框，选择图片
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片", "",
                                                   "Image Files (*.jpg *.png)", options=options)
        if file_name:
            self.image_path = file_name

    def startGenerate(self):
        if self.is_generating:
            return
        if not self.json_path or not self.image_path:
            QMessageBox.warning(self, '警告', '请选择JSON文件和图片!')
            return

        self.is_generating = True
        self.btn_generate.setText('生成中...')
        self.worker_thread = WorkerThread(self.json_path, self.image_path)
        self.worker_thread.generate_finished.connect(self.generateFinished)
        self.worker_thread.start()

    def generateFinished(self, cloud_image_path):
        self.is_generating = False
        self.btn_generate.setText('生成')
        QMessageBox.about(self, '提示', '生成完成！')
        # 检查图片路径是否存在
        if os.path.exists(cloud_image_path):
            pixmap = QPixmap(cloud_image_path)
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText('图片不存在！')

    def showImage(self):
        # 检查图片路径是否存在
        if os.path.exists(self.WordCloudimage_path):
            pixmap = QPixmap(self.WordCloudimage_path)
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText('图片不存在！')

    def wordCloudQss(self):
        self.btn_choose_json.setMinimumSize(100, 30)
        self.btn_choose_json.setStyleSheet(
            "QPushButton"
            "{"
            "font: 25 10pt '微软雅黑 Light';"
            "color: rgb(0,0,0);"
            "background-color: rgb(255,255,255);"
            "border: none;"
            "border-radius:4px;"
            "border: 1px solid rgb(200,200,200);"
            "}"
            "QPushButton:hover"
            "{"
            "background-color: rgb(235,235,236);"
            "}"
            "QPushButton:pressed"
            "{"
            "background-color: rgb(235,235,236);"
            "}"
        )

        self.btn_choose_image.setMinimumSize(100, 30)
        self.btn_choose_image.setStyleSheet(
            "QPushButton"
            "{"
            "font: 25 10pt '微软雅黑 Light';"
            "color: rgb(0,0,0);"
            "background-color: rgb(255,255,255);"
            "border: none;"
            "border-radius:4px;"
            "border: 1px solid rgb(200,200,200);"
            "}"
            "QPushButton:hover"
            "{"
            "background-color: rgb(235,235,236);"
            "}"
            "QPushButton:pressed"
            "{"
            "background-color: rgb(235,235,236);"
            "}"
        )

        self.btn_generate.setMinimumSize(100, 30)
        self.btn_generate.setStyleSheet(
            "QPushButton"
            "{"
            "font: 25 10pt '微软雅黑 Light';"
            "color: rgb(0,0,0);"
            "background-color: rgb(255,255,255);"
            "border: none;"
            "border-radius:4px;"
            "border: 1px solid rgb(200,200,200);"
            "}"
            "QPushButton:hover"
            "{"
            "color: rgb(255,255,255);"
            "background-color: rgb(78,110,242);"
            "}"
            "QPushButton:pressed"
            "{"
            "color: rgb(255,255,255);"
            "background-color: rgb(69,98,219);"
            "}"
        )