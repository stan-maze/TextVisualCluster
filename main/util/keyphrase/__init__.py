# -*- coding: utf-8 -*-

import os

CURRENT_PATH = os.path.abspath(__file__)
DATA_PATH = os.path.dirname(os.path.dirname(CURRENT_PATH))
FONT_PATH = os.path.join(DATA_PATH, "data", "simfang.ttf")
STOPWORDS = os.path.join(DATA_PATH, "data", "stop_words.txt")
# MASK_PATH = os.path.join(DATA_PATH, "data", "map.png")
# MASK_PATH = os.path.join(DATA_PATH, "data", "apple.png")
# MASK_PATH = os.path.join(DATA_PATH, "data", "love.png")