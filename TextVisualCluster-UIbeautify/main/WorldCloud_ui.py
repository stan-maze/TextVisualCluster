# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'WorldCloud_ui.ui'
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
from PySide6.QtWidgets import (QPushButton,
    QApplication, QMainWindow, QWidget, QLabel,
    QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QProgressBar, QDialog
)
import matplotlib
from matplotlib import pyplot as plt
from io import BytesIO

import os
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")

        # 创建布局
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 创建组件
        self.btn_choose_json = QPushButton("选择 JSON 文件")
        self.btn_choose_image = QPushButton("选择图片文件")
        self.image_label = QLabel()
        self.btn_generate = QPushButton("生成")

        # 将组件添加到布局中
        self.layout.addWidget(self.btn_choose_json)
        self.layout.addWidget(self.btn_choose_image)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.btn_generate)
        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
    # retranslateUi

