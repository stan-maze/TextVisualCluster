from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QFileDialog, QMessageBox, QLabel
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import QTimer

import json
import os
from util.json2text import JsonToTxtConverter
import subprocess
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

class ImageJsonGenerator():
    def __init__(self):
        self.WordCloudimage_path = os.path.join(PROJECT_DIR, f'wordcloud-master\love_test.png')
        # self.WordCloudimage_path = os.path.join(PROJECT_DIR, 'wordcloud-master')
        self.json2text = JsonToTxtConverter()
        self.window = QMainWindow()
        self.window.resize(750, 400)
        self.window.move(300, 300)
        self.window.setWindowTitle('图片和JSON生成器')

        self.json_path = ''
        self.image_path = ''

        # JSON文件选择按钮
        self.json_button = QPushButton('选择JSON文件', self.window)
        self.json_button.move(10, 25)
        self.json_button.clicked.connect(self.chooseJson)

        # 图片选择按钮
        self.image_button = QPushButton('选择图片', self.window)
        self.image_button.move(10, 60)
        self.image_button.clicked.connect(self.chooseImage)

        # 文本框显示JSON文件路径和图片路径
        self.textEdit = QPlainTextEdit(self.window)
        self.textEdit.setPlaceholderText("请选择JSON文件和图片")
        self.textEdit.move(10, 95)
        self.textEdit.resize(300, 250)

        # 生成按钮
        self.generate_button = QPushButton('生成', self.window)
        self.generate_button.move(340, 80)
        self.generate_button.clicked.connect(self.generate)
        
         # 图片显示框
        self.image_label = QLabel(self.window)
        self.image_label.setGeometry(480, 100, 240, 240)
        self.image_label.setScaledContents(True)
        # 置为不显示, 当有图片时显示
        self.image_label.setVisible(False)
        
        
        # 定时器，用于定期检查图片路径是否存在
        self.timer = QTimer(self.window)
        self.timer.timeout.connect(self.showImage)
        self.timer.start(1000)

    def chooseJson(self):
        # 使用Qt自带的文件选择框而不是操作系统的原生文件选择框
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self.window, "选择JSON文件", "",
                                                   "JSON Files (*.json)", options=options)
        if file_name:
            self.json_path = file_name
            self.updateText()

    def chooseImage(self):
        # 弹出文件选择框，选择图片
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self.window, "选择图片", "",
                                                   "Image Files (*.jpg *.png)", options=options)
        if file_name:
            self.image_path = file_name
            self.updateText()

    def updateText(self):
        # 更新文本框中的内容，显示JSON文件路径和图片路径
        text = f"JSON文件路径:\n{self.json_path}\n图片路径:\n{self.image_path}"
        self.textEdit.setPlainText(text)

    def generate(self):
        # 点击生成按钮，将图片链接和JSON文件链接传入响应函数中，并在消息框中显示链接信息
        if self.json_path and self.image_path:
            self.json2text.convert_to_txt_file(self.json_path)
            print(PROJECT_DIR)
            print(os.path.join(PROJECT_DIR, "wordcloud-master"))
            bat_file_path = os.path.join(os.path.dirname(self.json_path), "generateWordCloud.bat")
            subprocess.run([bat_file_path])

            # command = f'cd {os.path.join(PROJECT_DIR, "/wordcloud-master")}/wordcloud-master && ls && python3 create_word_cloud.py test.txt'
            # os.system(command)
            QMessageBox.about(self.window,
                              '提示',
                              f"文本由json给出\n词云样式由图片给出")
        else:
            QMessageBox.warning(self.window,
                                '警告',
                                '请选择JSON文件和图片!')
    
    def showImage(self):
        # 检查图片路径是否存在
        if self.WordCloudimage_path and os.path.exists(self.WordCloudimage_path):
            # print("FQ")
            pixmap = QPixmap(self.WordCloudimage_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.setVisible(True)
        else:
            self.image_label.setVisible(False)



app = QApplication([])
generator = ImageJsonGenerator()
generator.window.show()
app.exec_()
