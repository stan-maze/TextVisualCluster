from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QFileDialog, QMessageBox, QLabel, QDialog, QVBoxLayout, QTextEdit
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer, QThread, Signal

import json
import os
from util.json2text import JsonToTxtConverter
import subprocess

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

class WorkerThread(QThread):
    generate_finished = Signal(str)

    def __init__(self, json_path):
        super().__init__()
        self.json_path = json_path

    def run(self):
        json2text = JsonToTxtConverter()
        json2text.convert_to_txt_file(self.json_path)
        bat_file_path = os.path.join(os.path.dirname(self.json_path), "generateWordCloud.bat")
        subprocess.run([bat_file_path])
        self.generate_finished.emit('生成完成')

class ImageJsonGenerator(QDialog):
    def __init__(self):
        super().__init__()
        self.WordCloudimage_path = os.path.join(PROJECT_DIR, f'wordcloud-master\love_test.png')

        self.setWindowTitle("生成词云")

        # 创建布局
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 创建组件
        self.btn_choose_json = QPushButton("选择 JSON 文件")
        self.btn_choose_image = QPushButton("选择图片文件")
        self.image_label = QLabel()
        self.btn_generate = QPushButton("生成")

        # 将组件添加到布局中
        layout.addWidget(self.btn_choose_json)
        layout.addWidget(self.btn_choose_image)
        layout.addWidget(self.image_label)
        layout.addWidget(self.btn_generate)

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
        self.worker_thread = WorkerThread(self.json_path)
        self.worker_thread.generate_finished.connect(self.generateFinished)
        self.worker_thread.start()

    def generateFinished(self, message):
        self.is_generating = False
        self.btn_generate.setText('生成')
        QMessageBox.about(self, '提示', '生成完成！')
        self.showImage()

    def showImage(self):
        # 检查图片路径是否存在
        if os.path.exists(self.WordCloudimage_path):
            pixmap = QPixmap(self.WordCloudimage_path)
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText('图片不存在！')