# -*- coding: utf-8 -*-
"""
一些语法判断 func
"""


import os
from config import PROJECT_PATH

from utils.duration import Duration
import re
import numpy as np

prog_zaifa = re.compile('[^，]再发')
prog_banjiazhong = re.compile('[^再发][^伴|并]加重')

negative_words = ['否', '未', '不', '无']


def is_have_negative_word(sentence):
    """
    是否有否定词汇
    :param sentence:
    :return: bool
    """
    for str_ in negative_words:
        if str_ in sentence:
            return True
    return False


def is_begin_about_accompany(sentence):
    """
    positive: e.g. 伴有心悸
    negative: e.g. 无伴出汗、胸闷、气促，
    :param sentence:
    :return: bool
    """
    if sentence.strip().startswith('不##d 伴##v') \
            or sentence.strip().startswith('无##d 伴##v') \
            or sentence.strip().startswith('无伴##v') \
            or sentence.strip().startswith('不伴##v') \
            or sentence.strip().startswith('伴'):
        return True
    return False


def is_totally_useless(sentence):
    """
    什么有效信息都没有，（目前只考虑Symptom，Disease，还有duration，duration要自己去提取）
    :param sentence:
    :return: bool
    """
    duration = Duration.get_duration_re(sentence=sentence)

    if 'Symptom' not in sentence \
            and 'Disease' not in sentence \
            and not duration:
        return True
    else:
        return False


def is_begin_with_location(sentence):
    """
    缘患者于10天前无明显诱因出现活动后气促，伴胸闷，不伴胸痛，`位于心前区`，呈轻度压迫感
    一个逗号句子以"位于开头"
    :param sentence:
    :return: bool
    """
    if sentence.strip().startswith('位于##v'):
        return True
    return False


def is_with_scope(sentence):
    """
    胸骨后压迫感，`范围`约巴掌大小，无放射性疼痛，
    不一定是要在逗号句子的开头
    :param sentence:
    :return:
    """
    if '范围##n' in sentence:
        return True
    return False


def longest_common_substring(str1, str2):
    """
    获得两个字符串的最长子串
    """
    str1_length = len(str1)  # 获取第一个字符串的长度
    str2_length = len(str2)  # 获取第二个字符串的长度
    record = np.zeros(shape=(str1_length, str2_length),dtype=int)
    maxLen = 0  # 最大长度
    maxEnd = 0  # 结束的索引

    for i in range(str1_length):
        for j in range(str2_length):
            if str1[i] == str2[j]:  # 判断两个字符串对应的索引是否相同
                if i == 0 or j == 0:    # 判断是否是第一行或者是第一列
                    record[i][j] = 1    # 如果是则对应索引置一
                else:   # 如果不是对应的索引则为其左上角对应的元素加一
                    record[i][j] = record[i - 1][j - 1] + 1
            else:   # 如果字符串对应的元素不相同则置零
                record[i][j] = 0
            if record[i][j] > maxLen:   # 判断记录数值是否大于最大长度
                maxLen = record[i][j]
                maxEnd = i  # 将结束索引置为i
    return str1[maxEnd - maxLen + 1: maxEnd + 1]


def conbine_similar_terms(input):
    """
    合并同类项
    input是分词后的句子
    """
    items = input.split(' ')

    l = len(items)
    i = 0
    while i < l:
        candid = items[i]
        j = i + 1 if i + 1 < l else -1
        if j == -1:
            break
        # 如果下一个词的词性和当前的一致
        if items[j].split('##')[-1] == candid.split('##')[-1]:
            word1 = candid.split('##')[0]
            word2 = items[j].split('##')[0]
            common = longest_common_substring(word1, word2)
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
                    idx1 = word1.index(common)
                    idx2 = word2.index(common)
                    words = word1[0:idx1] + common + word2[idx2 + len(common):]
            # 没有相同的部分
            else:
                words = word1 + word2
            semantic = items[j].split('##')[-1]
            items[i] = words[:] + '##' + semantic
            del items[j]
            l -= 1
            i -= 1
        i += 1

    return " ".join(items)


def is_basic_info_status_related_sentence(sentence):
    """
    判断是否是处理basicInfo的句子
    :param sentence:
    :return: bool
    """
    if '##BasicInfo' in sentence and '##Status' in sentence:
        return True
    return False


if __name__ == '__main__':

    txt_path = os.path.join(PROJECT_PATH, 'data/data_main/chief_complaint_6_4.txt')
    with open(txt_path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    for line in data:
        origin, input = line.split('\t')
        print(conbine_similar_terms(input))

    '''  
    str1 = '左上腹'
    str2 = '部'
    lcs = longest_common_substring(str1, str2)
    print(lcs)
    
    input = '左上腹##Bodypart 上腹##Bodypart 上腹部##Bodypart 腹部##Bodypart 疼痛##Symptom 5##m +##x 小##a 时##ng 。##x'
    x = conbine_similar_terms(input)
    print(x)
    '''
