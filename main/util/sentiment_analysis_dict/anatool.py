# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 10:28:41 2020

@author: cm
"""

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))

# Add a subdirectory of this directory to the module search path
sys.path.append(script_dir)

print(sys.path)
from util.sentiment_analysis_dict.networks import SentimentAnalysis

SA = SentimentAnalysis()

class tool:
    def __init__(self):
        pass

    def predict(self, sent):
        """
        1: positif
        0: neutral
        -1: negatif
        """
        score1,score0 = SA.normalization_score(sent)
        if score1 == score0:
            result = 0
        elif score1 > score0:
            result = 1
        elif score1 < score0:
            result = -1
        return result
        

if __name__ =='__main__':
    text = '对你不满意'
    text = '大美女'
    text = '帅哥'
    text = '我妈说明儿不让出去玩'
    print(tool().predict(text))
