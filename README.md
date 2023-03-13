# TextVisualCluster

## 库
1. pip install -r requirement.txt
1. pyside6
1. wordcloud
1. jieba
1. pandas
1. openpyxl
1. pywin32


## 用法
python MainWindow.py

## 页面
1. MainWindow.py是主窗口, 第一个按钮选择excel文件, 第二个按钮待实现, 第三个按钮弹出词云窗口
1. WordCloud.py绘制词云, 负责将文本json和图片交付wordcloud-master, 然后显示保存的词云图片
1. Cluster.py绘制将聚类的json结果可视化展现

## 待完成
1. wordcloud-master需要改造成python模块, 主类(初始化或者主方法)接受两个参数, txt文本路径和图片路径, 返回词云图片路径, 建议将词云图片放入resource
2. 聚类结果保存为json格式, 详见resource/test.json
