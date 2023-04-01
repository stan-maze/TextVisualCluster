# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Cluster_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QSizePolicy, QWidget)
import sys
import json
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QBrush, QPen, QColor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QProgressBar, QDialog, QComboBox, QLineEdit, QPushButton, QScrollArea
)
import matplotlib
from matplotlib import pyplot as plt
from io import BytesIO

import os
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")

        Dialog.setMinimumSize(600, 618)
        # 3 设置组件的滚动区域
        self.scrollArea = QScrollArea(Dialog)
        # self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setMinimumSize(600, 618)
        self.scrollArea.setWidgetResizable(True)
        # 4 设置滚动区域的内容组件
        self.scrollAreaWidgetContents = QWidget()
        # 5 设置滚动区内容的布局方式
        self.layout = QVBoxLayout(self.scrollAreaWidgetContents)
        # 7 设置滚动区域显示内容
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # self.layout = QVBoxLayout(Dialog)

        self.algorithm_label = QLabel("选择聚类算法")
        self.combo_cluster = QComboBox()
        self.combo_cluster.addItem("kmeans")
        self.combo_cluster.addItem("dbscan")
        self.combo_cluster.setCurrentIndex(0)
        self.param_label = QLabel("设置k值：")
        self.param_lineedit = QLineEdit()
        self.param_lineedit.setText("6")
        self.btn_cluster = QPushButton("生成聚类")
        self.table = QTableWidget()
        self.image_label = QLabel()

        self.layout.addWidget(self.algorithm_label)
        self.layout.addWidget(self.combo_cluster)
        self.layout.addWidget(self.param_label)
        self.layout.addWidget(self.param_lineedit)
        self.layout.addWidget(self.btn_cluster)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.image_label)

        self.table.setVisible(False)

        self.table.setFixedSize(400, 200)
        self.image_label.setFixedSize(500, 400)

        # 创建表格
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['主题', '占比', '学生反响'])

        self.combo_cluster.currentIndexChanged.connect(self.show)


    # setupUi


    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
    # retranslateUi

    def show(self):
        if self.combo_cluster.currentText() == "kmeans":
            self.param_label.setText("设置k值：")
            self.param_lineedit.setText("6")
        elif self.combo_cluster.currentText() == "dbscan":
            self.param_label.setText("设置距离：")
            self.param_lineedit.setText("0.135")
