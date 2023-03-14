from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QPushButton, QFileDialog, QTextEdit,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
class my_ui(object):
    def setupUi(self, QMainWindow):
        self.setWindowTitle("预习帮手")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        # 创建布局
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        # 创建按钮
        self.btn_open_file = QPushButton("选择文件")
        self.layout.addWidget(self.btn_open_file)
        self.btn_cluster = QPushButton("生成聚类")
        self.layout.addWidget(self.btn_cluster)
        self.btn_wordcloud = QPushButton("生成词云")
        self.layout.addWidget(self.btn_wordcloud)
        # 创建文本框
        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)