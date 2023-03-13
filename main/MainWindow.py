import sys
import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QHBoxLayout
import WordCloud, Cluster

import os
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("预习帮手")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建布局
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # 创建按钮
        self.btn_open_file = QPushButton("选择文件")
        self.btn_open_file.clicked.connect(self.open_file)
        self.layout.addWidget(self.btn_open_file)

        self.btn_cluster = QPushButton("生成聚类")
        self.btn_cluster.clicked.connect(self.generate_cluster)
        self.btn_cluster.setDisabled(True)
        self.layout.addWidget(self.btn_cluster)

        self.btn_wordcloud = QPushButton("生成词云")
        self.btn_wordcloud.clicked.connect(self.generate_wordcloud)
        self.btn_wordcloud.setDisabled(True)
        self.layout.addWidget(self.btn_wordcloud)

        # 创建文本框
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)

    def open_file(self):
        # 打开文件选择对话框
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "Excel Files (*.xls *.xlsx)", options=options)

        if file_name:
            # 读取 Excel 文件内容
            df = pd.read_excel(file_name, engine='openpyxl')
            # 将 DataFrame 转换为字符串，并显示在文本框中
            text = df.to_string(index=True, justify='left')
            self.text_edit.setPlainText(text)

            # 启用生成聚类和词云的按钮
            self.btn_cluster.setDisabled(False)
            # 
            self.btn_wordcloud.setDisabled(False)


    def generate_cluster(self):
        # 弹出新窗口，生成聚类
        
        self.setEnabled(False)
        cluster = Cluster.Cluster()
        cluster.exec()
        self.setEnabled(True)
        pass

    def generate_wordcloud(self):
        # 弹出新窗口，生成词云
        self.setEnabled(False)
        wordcloud = WordCloud.ImageJsonGenerator()
        wordcloud.exec()
        self.setEnabled(True)
        # pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
