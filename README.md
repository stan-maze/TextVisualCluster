# TextVisualCluster

## 库
pyside2/pyside6
wordcloud
jieba
pandas
openpyxl


## 用法
python word_cloud.py
## 页面
MainWindow.py是主窗口, 第一个按钮选择excel文件, 第二个按钮待实现, 第三个按钮弹出词云窗口
word_cloud.py绘制词云, 负责将文本json和图片交付wordcloud-master, 然后绘制得到的词云图片
## 待完成
wordcloud-master需要改造成python模块, 主类(初始化或者主方法)接受两个参数, txt文本路径和图片路径, 返回词云图片路径, 建议将词云图片放入resource

