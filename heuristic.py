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


import requests

def gen_links(page_link):
    res = requests.get(page_link)
    soup = BeautifulSoup(res.content, 'html.parser')

    links = soup.find_all('a')

    results = []

    for link in links:
        if link.has_attr('href'):
            linked_page_url = link['href']
            if linked_page_url.startswith('/wiki') and ':' not in linked_page_url:
                # print(linked_page_url)
                results.append("https://en.wikipedia.org" + linked_page_url)

    return list(set(results))


def get_best_class(link: str):
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
    return highest_class[0]


def fetch_page(link):
    html = urllib.request.urlopen(link).read()
    print("Fetched webpage")
    text = [text_from_html(html)]
    return text


def get_utility(text, class_):
    open("test", "w").write(text[0])

    pipe_file = open("pipe", "rb")
    pca_file = open("pca", "rb")
    model_file = open("model", "rb")

    pipe = pickle5.load(pipe_file)
    pca = pickle5.load(pca_file)
    gnb = pickle5.load(model_file)

    test_data = pipe.transform(text)
    pca_test_data = pca.transform(test_data.toarray())

    index = list(gnb.classes_).index(class_)

    probabilties = gnb.predict_proba(pca_test_data)
    print("Processed webpage")
    # print(probabilties)
    return probabilties[0][index]


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Metal"
    # url2 = "https://en.wikipedia.org/wiki/Coimbatore_International_Airport"

    # best_class = get_best_class(url)

    # print(get_utility(url2, best_class))

    # print(get_best_class(url2))

    print(gen_links(url))
    print(len(gen_links(url)))
