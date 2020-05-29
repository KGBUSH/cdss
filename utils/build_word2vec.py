# -*- coding: utf-8 -*-
import re
import os
from gensim.models import Word2Vec
from config import PROJECT_PATH

"""
构建word to vector
"""


def _load_corpus(txt_path):

    data = []

    with open(txt_path, 'r', encoding='utf-8') as fr:
        lines_num = len(fr.readlines())

    sample_f = open(txt_path, 'r', encoding='utf-8')
    for i in range(int(lines_num)):
        line = sample_f.readline()
        line = line.strip('\n').strip()
        line = line.replace(',', '，')
        if line == '':
            continue
        try:
            origin, input_ = line.split('\t')[0], line.split('\t')[-1]
            data.append(input_)
        except:
            pass

    return data


def _parse_one_sent(sent):

    if '小##a 时##ng' in sent:
        sent = sent.replace('小##a 时##ng', '小时##m')

    if '年##m 余##m' in sent:
        sent = sent.replace('年##m 余##m', '年余##m')

    words = sent.split()
    s = ''
    for word in words:
        if re.search("[a-zA-Z]", word.split('##')[0]):
            s += word.split('##')[0] + ' '
        else:
            tmp = word.split('##')[0]
            tmp = re.sub("[!@$%^&*()_+\-=[\]{}''\"/<>,.，。！、‘”’“？：；;:（）°~·`]+", "#CHAR#", tmp)
            s += re.sub("[0-9]+", "#NUM#", tmp) + ' '

    return s


if __name__ == '__main__':
    txt_path = os.path.join(PROJECT_PATH, 'data/cur_medical_segment.txt')
    data = _load_corpus(txt_path)
    corpus = []
    for sent in data:
        corpus.append(_parse_one_sent(sent).split())
    model = Word2Vec(corpus, size=32, window=5, min_count=1, workers=4)
    print(model.wv.vectors.shape)
