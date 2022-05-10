from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import pickle5

import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
import string
from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split

class LemmaTokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

# from pgmpy.models import NaiveBayes
from sklearn import decomposition
from sklearn.metrics import roc_auc_score

from nltk.corpus import stopwords
import nltk


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def get_heuristic(link: str):
    html = urllib.request.urlopen(link).read()
    text = [text_from_html(html)]

    open("test", "w").write(text[0])

    pipe_file = open("pipe", "rb")
    pca_file = open("pca", "rb")
    model_file = open("model", "rb")

    pipe = pickle5.load(pipe_file)
    pca = pickle5.load(pca_file)
    gnb = pickle5.load(model_file)

    test_data = pipe.transform(text)
    pca_test_data = pca.transform(test_data.toarray())

    highest_class = gnb.predict(pca_test_data)
    index = list(gnb.classes_).index(highest_class)


    probabilties = gnb.predict_proba(pca_test_data)
    return probabilties[0][index]


if __name__ == "__main__":
    URL = "https://en.wikipedia.org/wiki/Telecommunications"
    get_heuristic(URL)

