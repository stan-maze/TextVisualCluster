from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QFileDialog, QMessageBox, QLabel, QDialog, QVBoxLayout, QTextEdit
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer, QThread, Signal

import json
import os
from util.json2text import JsonToTxtConverter
import subprocess 
import WordCloudMaster.create_word_cloud as cwc

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    def test():
        main_path = os.path.abspath(os.path.join(PROJECT_DIR, os.pardir))
        print(main_path)
        text_path = os.path.join(main_path, 'main','resource', 'test.txt')
        pic_path = os.path.join(main_path, 'main','resource', 'love.png')
        print(pic_path)
        result_path = cwc.create_wordscloud(text_path, pic_path)
        print(result_path)
    test()