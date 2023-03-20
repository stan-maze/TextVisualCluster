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


        self.layout = QVBoxLayout(Dialog)


        self.table = QTableWidget()
        self.image_label = QLabel()

        self.layout.addWidget(self.table)
        self.layout.addWidget(self.image_label)


        self.table.setFixedSize(400, 200)
        self.image_label.setFixedSize(500, 400)

        # 创建表格
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['主题', '占比', '学生反响'])


    # setupUi


    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
    # retranslateUi

