import jieba
import codecs
import sys
import pandas
import numpy as np
from wordcloud import WordCloud
import imageio
from wordcloud import WordCloud, ImageColorGenerator
from os import listdir
from os.path import isfile, join

#停止词文件目录
stopwords_filename = 'data/stopwords.txt'
#字体文件目录
font_filename = 'fonts/STFangSong.ttf'
#词云图片输出目录
template_dir = 'data/templates/'
#词云背景颜色
word_background_color='white'
#字体最大大小
word_size=600

#分词过滤函数
def cut(input_filename):
    content = '\n'.join([line.strip()
                         for line in codecs.open(input_filename, 'r', 'utf-8')
                         if len(line.strip()) > 0])
    stopwords = set([line.strip()
                     for line in codecs.open(stopwords_filename, 'r', 'utf-8')])

    segs = jieba.cut(content)
    words = []
    for seg in segs:
        word = seg.strip().lower()
        if len(word) > 1 and word not in stopwords:
            words.append(word)
    return words

#词语出现次数统计函数
def word_counting(words):
    
    #创建由分词过滤后的词语表格words_df。
    words_df = pandas.DataFrame({'word': words})
    #统计词语出现的次数
    words_stat = words_df.groupby(by=['word'])['word'].agg(np.size)
    words_stat = words_stat.to_frame()
    #按词语出现的次数重排表格
    words_stat.columns = ['number']
    words_stat = words_stat.reset_index().sort_values(by="number", ascending=False)
    return words_stat

#生成词云函数
def create_wordscloud(input_filename):
    words=cut(input_filename)
    words_stat=word_counting(words)
    print('# of different words =', len(words_stat))
    input_prefix = input_filename
    if input_filename.find('.') != -1:
        input_prefix = '.'.join(input_filename.split('.')[:-1])

    for file in listdir(template_dir):
        if file[-4:] != '.png' and file[-4:] != '.jpg':
            continue
        background_picture_filename = join(template_dir, file)
        if isfile(background_picture_filename):
            prefix = file.split('.')[0]

            bimg = imageio.imread(background_picture_filename)
            wordcloud = WordCloud(font_path=font_filename, background_color=word_background_color,
                                  mask=bimg, max_font_size=word_size, random_state=100)
            wordcloud = wordcloud.fit_words(
                dict(words_stat.head(100).itertuples(index=False)))

            bimgColors = ImageColorGenerator(bimg)
            wordcloud.recolor(color_func=bimgColors)

            output_filename = prefix + '_' + input_prefix + '.png'

            print('Saving', output_filename)
            wordcloud.to_file(output_filename)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        create_wordscloud(sys.argv[1])
    else:
        print('[usage] <input>')
