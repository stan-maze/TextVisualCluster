# -*- coding: utf-8 -*-

import jieba
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
from util.text_cluster import STOPWORDS



def mysimple_segment(text):
    """
    简单的中文分词方法，基于规则
    :param text: 待分词的中文文本
    :return: 分词后的文本列表
    """
    # 定义标点符号和连续数字的正则表达式
    punctuation = r'[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+'
    digits = r'\d+'

    # 去除标点符号和数字
    text = re.sub(punctuation, '', text)
    text = re.sub(digits, '', text)

    # 使用jieba分词库分词
    words = jieba.cut(text)

    # 过滤停用词
    result = [word for word in words if word not in stopwords]

    return result


class myVectorizer():
    def __init__(self):
        self.vocab = {}

    def fit(self, corpus):
        """
        构建词汇表
        :param corpus: 语料列表，每个元素为一篇文本
        :return: None
        """
        for text in corpus:
            for word in text.split():
                if word not in self.vocab:
                    self.vocab[word] = len(self.vocab)

    def transform(self, corpus):
        """
        将文本列表转化为向量列表
        :param corpus: 语料列表，每个元素为一篇文本
        :return: 向量列表，每个元素为一个向量
        """
        result = []
        for text in corpus:
            vector = [0] * len(self.vocab)
            for word in text.split():
                if word in self.vocab:
                    vector[self.vocab[word]] += 1
            result.append(vector)
        return result


class myKMeans():
    def __init__(self, n_clusters, max_iter=300):
        """
        初始化 KMeans 模型
        :param n_clusters: 簇的数量
        :param max_iter: 最大迭代次数
        """
        self.n_clusters = n_clusters
        self.max_iter = max_iter

    def fit(self, X):
        """
        训练 KMeans 模型
        :param X: 输入数据，每个元素为一个向量
        :return: None
        """
        # 随机初始化聚类中心
        self.centroids = X[np.random.choice(X.shape[0], self.n_clusters, replace=False)]

        for _ in range(self.max_iter):
            # 分配样本到最近的聚类中心
            labels = self.assign_labels(X)

            # 计算新的聚类中心
            new_centroids = np.array([X[labels == i].mean(axis=0) for i in range(self.n_clusters)])

            # 如果聚类中心不再发生变化，则停止迭代
            if np.allclose(self.centroids, new_centroids):
                break

            # 更新聚类中心
            self.centroids = new_centroids

    def predict(self, X):
        """
        预测新数据的聚类标签
        :param X: 输入数据，每个元素为一个向量
        :return: 聚类标签
        """
        distances = [np.linalg.norm(X - centroid, axis=1) for centroid in self.centroids]
        labels = np.argmin(distances, axis=0)
        return labels

    def assign_labels(self, X):
        """
        分配样本到最近的聚类中心
        :param X: 输入数据，每个元素为一个向量
        :return: 聚类标签
        """
        distances = [np.linalg.norm(X - centroid, axis=1) for centroid in self.centroids]
        labels = np.argmin(distances, axis=0)
        return labels



class KmeansClustering():
    def __init__(self, stopwords_path=STOPWORDS):
        self.stopwords = self.load_stopwords(stopwords_path)
        self.vectorizer = CountVectorizer()
        self.transformer = TfidfTransformer()

    def load_stopwords(self, stopwords=None):
        """
        加载停用词
        :param stopwords:
        :return:
        """
        if stopwords:
            with open(stopwords, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f]
        else:
            return []

    def preprocess_data(self, corpus_path):
        """
        文本预处理，每行一个文本
        :param corpus_path:
        :return:
        """
        corpus = []
        with open(corpus_path, 'r', encoding='utf-8') as f:
            for line in f:
                corpus.append(' '.join([word for word in jieba.lcut(line.strip()) if word not in self.stopwords]))
        return corpus

    def get_text_tfidf_matrix(self, corpus):
        """
        获取tfidf矩阵
        :param corpus:
        :return:
        """
        tfidf = self.transformer.fit_transform(self.vectorizer.fit_transform(corpus))

        # 获取词袋中所有词语
        # words = self.vectorizer.get_feature_names()

        # 获取tfidf矩阵中权重
        weights = tfidf.toarray()
        return weights

    def kmeans(self, corpus_path, n_clusters=5):
        """
        KMeans文本聚类
        :param corpus_path: 语料路径（每行一篇）,文章id从0开始
        :param n_clusters: ：聚类类别数目
        :return: {cluster_id1:[text_id1, text_id2]}
        """
        corpus = self.preprocess_data(corpus_path)
        weights = self.get_text_tfidf_matrix(corpus)

        clf = KMeans(n_clusters=n_clusters)

        # clf.fit(weights)

        y = clf.fit_predict(weights)

        # 中心点
        # centers = clf.cluster_centers_

        # 用来评估簇的个数是否合适,距离约小说明簇分得越好,选取临界点的簇的个数
        # score = clf.inertia_

        # 每个样本所属的簇
        result = {}
        for text_idx, label_idx in enumerate(y):
            key = "cluster_{}".format(label_idx)
            if key not in result:
                result[key] = [text_idx]
            else:
                result[key].append(text_idx)
        return result


if __name__ == '__main__':
    Kmeans = KmeansClustering(stopwords_path='../data/stop_words.txt')
    result = Kmeans.kmeans('../data/test_data.txt', n_clusters=5)
    print(result)