from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QFileDialog, QMessageBox, QLabel, QDialog, QVBoxLayout, QTextEdit
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer, QThread, Signal

import json
import os
from util.json2text import JsonToTxtConverter
import subprocess 
from WordCloudMaster import create_word_cloud as CWC

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    def test():
        main_path = os.path.abspath(os.path.join(PROJECT_DIR, os.pardir))
        text_path = os.path.join(main_path, 'resource', 'test.txt')
        pic_path = os.path.join(main_path, 'resource', 'love.png')
        result_path = CWC.create_wordscloud(text_path, pic_path)
        print(result_path)
    test()