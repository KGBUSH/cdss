# -*- coding: utf-8 -*-
import os
from config import PROJECT_PATH

"""
一些语法判断 func
"""
from utils.duration import Duration
import re

prog_zaifa = re.compile('[^，]再发')
prog_banjiazhong = re.compile('[^再发][^伴|并]加重')




def is_begin_with_no_accompany(sentence):
    """
    e.g. 无伴出汗、胸闷、气促，
    :param sentence:
    :return:
    """
    if sentence.strip().startswith('不##d 伴##v') \
            or sentence.strip().startswith('无##d 伴##v') \
            or sentence.strip().startswith('无伴##v') \
            or sentence.strip().startswith('不伴##v'):
        return True
    return False


def is_totally_useless(sentence):
    """
    什么有效信息都没有，（目前只考虑Symptom，Disease，还有duration，duration要自己去提取）
    :param sentence:
    :return:
    """
    duration = Duration.get_duration_re(sentence=sentence)

    if 'Symptom' not in sentence \
            and 'Disease' not in sentence\
            and not duration:
        return True
    else:
        return False


def is_begin_with_location(sentence):
    """
    缘患者于10天前无明显诱因出现活动后气促，伴胸闷，不伴胸痛，`位于心前区`，呈轻度压迫感
    一个逗号句子以"位于开头"
    :param sentence:
    :return:
    """
    if sentence.strip().startswith('位于##v'):
        return True
    return False


def conbine_similar_terms(input):
    items = input.split(' ')
    new_items = []
    l = len(items)
    i = 0
    while i < l:
        candid = items[i]
        j = i+1 if i+1 < l else l-1
        # 如果下一个词的词性和当前的一致
        if items[j].split('##')[-1] == candid.split('##')[-1] :
            word1 = candid.split('##')[0]
            word2 = items[j].split('##')[0]
            common = ''.join(set(word1).intersection(set(word2)))
            words = ''
            # 有相同的部分
            if len(common) > 0:
                # 相同的部分正好是word1
                if len(common) == len(word1):
                    words = word2
                # 相同的部分正好是word2
                elif len(common) == len(word2):
                    words = word1
                # 相同的部分是word1后半部和word2前半部
                else:
                    # 如果相同部分不相连，会出事
                    # e.g 左胸疼痛 和 左胸痛
                    try:
                        idx1 = word1.index(common)
                        idx2 = word2.index(common)
                        words = word1[0:idx1] + common + word2[idx2+len(common):]
                    except:
                        words = word1 + word2

            # 没有相同的部分
            else:
                words = word1 + word2
            semantic = items[j].split('##')[-1]
            items[i] = words[:]+'##'+semantic
            del items[j]
            l -= 1
            i -= 1
        i += 1

    return " ".join(items)


if __name__ == '__main__':
    txt_path = os.path.join(PROJECT_PATH, 'data/data_main/chief_complaint_6_4.txt')
    with open(txt_path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    for line in data:
        origin, input = line.split('\t')
        print(conbine_similar_terms(input))
