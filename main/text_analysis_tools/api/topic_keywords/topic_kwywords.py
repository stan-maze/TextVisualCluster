# -*- coding: utf-8 -*-

import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation



class TopicKeywords:
    
    def __init__(self, train_data, n_components=10, n_top_words=50, max_iter=50):
        self.train_data = [" ".join(jieba.lcut(data)) for data in train_data]
        self.n_components = n_components
        self.n_top_words = n_top_words
        self.max_iter = max_iter

    def print_top_words(self, model, feature_names, n_top_words):
        ret = {}
        for topic_idx, topic in enumerate(model.components_):
            key = "topic_{}".format(topic_idx)
            val = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
            ret[key] = val
        return ret

    def analysis(self):
        tf_vectorizer = CountVectorizer()

        tf = tf_vectorizer.fit_transform(self.train_data)

        lda = LatentDirichletAllocation(n_components=self.n_components, max_iter=self.max_iter,
                                        learning_method='online',
                                        learning_offset=50.,
                                        random_state=0)
        lda.fit(tf)
        tf_feature_names = None
        if hasattr(tf_vectorizer, "get_feature_names"):
            tf_feature_names = tf_vectorizer.get_feature_names()
        else:
            tf_feature_names = tf_vectorizer.get_feature_names_out()
        return self.print_top_words(lda, tf_feature_names, self.n_top_words)