# -*- coding: utf-8 -*-

import jieba
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from util.text_cluster import STOPWORDS


class mySimpleTokenizer:
    def __init__(self, dict_path=None):
        self.dict = {}
        if dict_path:
            with open(dict_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word, freq = line.strip().split()
                    self.dict[word] = int(freq)

    def cut(self, text):
        result = []
        i = 0
        while i < len(text):
            word = None
            for j in range(len(text), i, -1):
                if text[i:j] in self.dict:
                    word = text[i:j]
                    result.append(word)
                    break
            if word is None:
                j = i + 1
                result.append(text[i:j])
            i = j
        return result


class myCountVectorizer:
    def __init__(self):
        self.vocab = set()
        self.word2idx = {}

    def fit(self, corpus):
        for doc in corpus:
            for word in doc.split():
                self.vocab.add(word)
        self.word2idx = {w: i for i, w in enumerate(self.vocab)}

    def transform(self, corpus):
        matrix = np.zeros((len(corpus), len(self.vocab)))
        for i, doc in enumerate(corpus):
            for word in doc.split():
                if word in self.vocab:
                    matrix[i, self.word2idx[word]] += 1
        return matrix

class myPCA:
    def __init__(self, n_components):
        self.n_components = n_components

    def fit_transform(self, X):
        X = X - np.mean(X, axis=0)
        U, S, Vt = np.linalg.svd(X, full_matrices=False)
        V = Vt.T
        components = V[:, :self.n_components]
        return np.dot(X, components)


class myDBSCAN:
    def __init__(self, eps, min_samples):
        self.eps = eps
        self.min_samples = min_samples
        self.labels = None
        self.visited = set()
        self.neighbors = {}
        
    def _expand_cluster(self, point_id, cluster_id):
        self.labels[point_id] = cluster_id
        neighbors = self.neighbors[point_id]
        for neighbor_id in neighbors:
            if neighbor_id not in self.visited:
                self.visited.add(neighbor_id)
                neighbor_neighbors = self.neighbors[neighbor_id]
                if len(neighbor_neighbors) >= self.min_samples:
                    neighbors |= neighbor_neighbors
            if self.labels[neighbor_id] is None:
                self.labels[neighbor_id] = cluster_id
    
    def fit_predict(self, X):
        self.labels = [None] * len(X)
        for i in range(len(X)):
            if i in self.visited:
                continue
            self.visited.add(i)
            neighbors = self.neighbors.get(i, set())
            if len(neighbors) < self.min_samples:
                continue
            cluster_id = len(self.labels) + 1
            self._expand_cluster(i, cluster_id)
        return self.labels


class DbscanClustering:
    def __init__(self):
        self.stopwords = self.load_stopwords(STOPWORDS)   # 加载停用词
        self.vectorizer = CountVectorizer()                # 定义计数向量器
        self.transformer = TfidfTransformer()              # 定义tf-idf转换器

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
                # 使用jieba分词对文本进行分词，并去除停用词
                corpus.append(' '.join([word for word in jieba.lcut(line.strip()) if word not in self.stopwords]))
        print(f"\n\ncorpus: {corpus} \n\n")
        return corpus

    def get_text_tfidf_matrix(self, corpus):
        """
        获取tfidf矩阵
        :param corpus:
        :return:
        """
        # 计数向量化器
        # 第_个列表元素, 词典中索引为_的元素, 词频为_
        vec_corpus = self.vectorizer.fit_transform(corpus)
        print(vec_corpus)
        # 在 TF-IDF 向量化中，每个向量的维度和计数向量化一样，但是值表示该词语在该文本中的 TF-IDF 权重。
        # 字词的重要性与其在文本中出现的频率成正比(TF)，与其在语料库中出现的频率成反比(IDF)
        tfidf = self.transformer.fit_transform(vec_corpus)

        # 获取词袋中所有词语
        # words = self.vectorizer.get_feature_names()

        # 获取tfidf矩阵中权重
        weights = tfidf.toarray()
        return weights

    def pca(self, weights, n_components=3):
        """
        PCA对数据进行降维
        :param weights:
        :param n_components:
        :return:
        """
        pca = PCA(n_components=n_components)
        return pca.fit_transform(weights)

    def dbscan(self, corpus_path, eps=0.1, min_samples=3, fig=False):
        """
        DBSCAN：基于密度的文本聚类算法
        :param corpus_path: 语料路径，每行一个文本
        :param eps: DBSCA中半径参数
        :param min_samples: DBSCAN中半径eps内最小样本数目
        :param fig: 是否对降维后的样本进行画图显示
        :return:
        """
        corpus = self.preprocess_data(corpus_path)
        weights = self.get_text_tfidf_matrix(corpus)

        pca_weights = self.pca(weights)

        clf = DBSCAN(eps=eps, min_samples=min_samples)

        y = clf.fit_predict(pca_weights)

        if fig:
            plt.scatter(pca_weights[:, 0], pca_weights[:, 1], c=y)
            plt.show()

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
    dbscan = DbscanClustering(stopwords_path='../data/stop_words.txt')
    result = dbscan.dbscan('../data/test_data.txt', eps=0.05, min_samples=3)
    print(result)
