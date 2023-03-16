import sys
import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QPushButton, QFileDialog, QTextEdit, 
    QVBoxLayout, QHBoxLayout, QMessageBox,
    QStackedWidget
)
import WordCloud, Cluster
from util.Converter import XlsxToTxtConverter
xlsxconv = XlsxToTxtConverter()
from util.cluster_theme import ClusterTool
clustertool = ClusterTool()
import re
import xlrd
import openpyxl
import os
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

###导入分离的ui文件
from main_ui import Ui_MainWindow

class MainWindow(Ui_MainWindow,QMainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()
        ##调用ui
        self.setupUi(self)

        self.xlsx_file_path = None
        self.txt_file_path = None
        self.json_file_path = None

        ##初始化控件

        self.btn_cluster.setDisabled(True)
        self.btn_open_file.clicked.connect(self.open_file)
        self.btn_cluster.clicked.connect(self.generate_cluster)
        self.btn_wordcloud.clicked.connect(self.generate_wordcloud)
        self.text_edit.setReadOnly(True)
        self.btn_wordcloud.setDisabled(True)

    def open_file(self):
        # 打开文件选择对话框
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "Excel Files (*.xls *.xlsx)", options=options)

        if file_name:
            self.xlsx_file_path = file_name
            # 读取 Excel 文件内容
            data = []
            if file_name.endswith('.xls'):
                workbook = xlrd.open_workbook(self.xlsx_file_path)
                sheet = workbook.sheet_by_index(0)
                data = [str(cell.value) for row in range(sheet.nrows) for cell in sheet.row(row)]
            else:
                workbook = openpyxl.load_workbook(self.xlsx_file_path, data_only=True)
                sheet = workbook.active
                data = [str(cell.value) for row in sheet.iter_rows() for cell in row]

            def remove_html_tags(text):
                # 去除html标签
                TAG_RE = re.compile(r'<[^>]+>')
                return TAG_RE.sub('', text)
            # 去除空行
            data = [text for text in data if text.strip() != '']
            # 去除html标签
            data = [remove_html_tags(text) for text in data]
            text = '\n'.join(data)
            
            self.text_edit.setPlainText(text)

            # 转换txt保存
            self.txt_file_path = xlsxconv.convert_to_txt_file(file_name)

            # 启用生成聚类和词云的按钮
            self.btn_cluster.setDisabled(False)
            self.btn_wordcloud.setDisabled(False)




    def generate_cluster(self):
        # 删除刷新
        for i in range(self.stackedWidget.count()):
            self.stackedWidget.removeWidget(  self.stackedWidget.widget(i))
        #self.setEnabled(False)
        # 执行聚类保存到相应json
        json_file_path = clustertool.excuteCluster(self.txt_file_path)
        # 显示提示信息
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(f"聚类成功，数据保存在 '{json_file_path}'")
        msg_box.setWindowTitle("提示")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()
        cluster = Cluster.Cluster(json_file_path)
        self.stackedWidget.addWidget(cluster)
        #self.setEnabled(True)

    def generate_wordcloud(self):
        # 弹出新窗口，生成词云
        #self.setEnabled(False)
        for i in range(self.stackedWidget.count()):
            self.stackedWidget_2.removeWidget(self.stackedWidget.widget(i))
        wordcloud = WordCloud.ImageJsonGenerator()
        self.stackedWidget_2.addWidget(wordcloud)
        #self.setEnabled(True)
        # pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
