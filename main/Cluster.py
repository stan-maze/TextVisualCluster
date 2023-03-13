import sys
import json
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QBrush, QPen, QColor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QProgressBar, QDialog
)
import matplotlib
from matplotlib import pyplot as plt
from io import BytesIO
import os
# 否则matplotlib和qt的图像引擎冲突
matplotlib.use('agg')
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


class Cluster(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("JSON可视化")
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table = QTableWidget()
        self.image_label = QLabel()

        layout.addWidget(self.table)
        layout.addWidget(self.image_label)
        
        self.setFixedSize(500, 600)
        self.table.setFixedSize(400, 200)
        self.image_label.setFixedSize(500, 400)

        # 创建表格
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['主题', '占比'])
        

        # 读取JSON文件
        with open(os.path.join(PROJECT_DIR, 'resource', 'test.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 填充表格
        percentages = []
        themes = []
        for row, item in enumerate(data):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(item['theme']))
            text_percentage = round(int(item['num']) / sum([x['num'] for x in data]) * 100, 2)
            percentages.append(text_percentage)
            themes.append(item['theme'])
            # 创建百分比条和文本标签
            progress_bar = QProgressBar()
            progress_bar.setValue(text_percentage)
            label = QLabel(str(text_percentage) + '%')
            # 创建布局，并将百分比条和文本标签添加到其中
            hbox = QHBoxLayout()
            hbox.addWidget(label)
            hbox.addWidget(progress_bar)
            hbox.setContentsMargins(0, 0, 0, 0)
            hbox.setAlignment(Qt.AlignCenter)
            # 将布局添加到表格中
            widget = QWidget()
            widget.setLayout(hbox)
            self.table.setCellWidget(row, 1, widget)

        # 生成饼状图
        fig, ax = plt.subplots()
        ax.pie(percentages, labels=themes, autopct='%1.1f%%')
        ax.axis('equal')  # 使饼状图为正圆形

        # 将生成的饼状图转换为pixmap，并设置为label的背景图片
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        # 动态伸缩
        self.image_label.setScaledContents(True)
        
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Cluster()
    window.show()
    sys.exit(app.exec())
