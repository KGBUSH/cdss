# -*- coding: utf-8 -*-

"""

@file: lda.py

@time: 2020/5/28 18:08

@desc: lda 暂时没用，就是分析一下

"""
import os
import re
from gensim import corpora, models
# from utils.build_word2vec import _load_corpus, _parse_one_sent
from config import PROJECT_PATH

useful = []  # 需要关注的词性

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


def lda(txt_path):
    """
    原始文本
    """
    # 1. 语料
    data = _load_corpus(txt_path)
    origin_corpus = []  # [['患者', '小时', ...], [], ...]
    for sent in data:
        origin_corpus.append(_parse_one_sent(sent).split())

    # 2.
    # 去重，存到字典
    dictionary = corpora.Dictionary(origin_corpus)
    dictionary.filter_n_most_frequent(5)
    # print(dictionary)
    corpus = [dictionary.doc2bow(words) for words in origin_corpus]
    # print(corpus)
    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10)
    for topic in lda.print_topics(num_words=10):
        print(topic)
    # 主题推断
    # print(lda.inference(corpus))
    # text5 = '中国女排将在郎平的率领下向世界女排三大赛的三连冠发起冲击'
    # bow = dictionary.doc2bow([word.word for word in jp.cut(text5) if word.flag in flags and word.word not in stopwords])
    # ndarray = lda.inference([bow])[0]
    # print(text5)
    # for e, value in enumerate(ndarray[0]):
    #     print('\t主题%d推断值%.2f' % (e, value))
    #
    # word_id = dictionary.doc2idx(['体育'])[0]
    # for i in lda.get_term_topics(word_id):
    #     print('【长途】与【主题%d】的关系值：%.2f%%' % (i[0], i[1]*100))


if __name__ == '__main__':
    txt_path = os.path.join(PROJECT_PATH, 'data/cur_medical_segment.txt')

    lda(txt_path=txt_path)

    # model = Word2Vec(corpus, size=32, window=5, min_count=1, workers=4)
    # print(model.wv.vectors.shape)
