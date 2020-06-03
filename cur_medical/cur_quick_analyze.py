# -*- coding: utf-8 -*-

"""

@file: cur_quick_analyze.py

@time: 2020/5/28 14:02

@desc: 把主诉那套quick_analyze.py的rules拿过来看看效果

"""

from config import PROJECT_PATH
from utils.duration import Duration
from utils.extension import Extension
from utils.visualize import View
from utils.grammar import is_begin_with_no_accompany, is_totally_useless

from chief_complaint.main_quick_analyze import parse_general_douhao_sentence, parse_dunhao_sentence

import os
import re

prog_zaifa = re.compile('[^，]再发')


def load_txt(txt_path):
    """
    e.g. /Users/dengyang/PycharmProjects/cdss/data/main_complaint_segment.txt
    """
    # 1. 按行load文件
    lines_num = -1
    with open(txt_path, 'r', encoding='utf-8') as fr:
        lines_num = len(fr.readlines())

    sample_f = open(txt_path, 'r', encoding='utf-8')
    print("load samples from %s ... ..." % txt_path)
    for i in range(int(lines_num)):
        line = sample_f.readline()
        line = line.strip('\n').strip()
        line = line.replace(',', '，')
        line = line.replace('；', '。')
        if line == '':
            continue
        try:
            origin, input = line.split('\t')[0], line.split('\t')[-1]  # 真正的input是分好词的，（line的后面一部分）
            if prog_zaifa.search(origin) is not None:
                input = input.replace('再发##ext_freq', '，##x 再发##ext_freq')
            all_results = parse_one_input(input=input)

            View.visualize(origin, all_results, mode='non-void')
        except:
            pass



def parse_one_input(input):
    """
    一整句input，可能包含句号
    :param input:
    :return:
    """
    # split 句号
    all_results = []  # 所有句号句子
    input_list = input.strip().strip('。##x').split('。##x')  # 先把最后的句号删了，再split by 句号

    for sentence in input_list:  # 句号句子
        # 1. 初始化句号句子的result
        results = {}  # {0:[dict,dict], 1:[]}  # 0, 1代表第几个逗号句子
        for c in range(sentence.count('，') + 1):
            results.update({c: []})

        # 2. 处理句号句子中的逗号句子
        douhao_list = sentence.split('，##x')
        for i in range(len(douhao_list)):
            douhao_sentence = douhao_list[i]
            parse_douhao_sentence(index=i, douhao_sentence=douhao_sentence, results=results)
        all_results.append(results)
    return all_results


def parse_douhao_sentence(index, douhao_sentence, results):
    """
    逗号句子总入口
    :param index: 这是这个句号句子里面的第几个逗号句子
    :param douhao_sentence: 逗号句子
    :param results: 句号句子层面，# {0:[dict,dict], 1:[]}  # 0, 1代表第几个逗号句子
    :return:
    """
    if is_totally_useless(sentence=douhao_sentence):
        results[index] = []  # 这句话没有有效词，就空吧

    elif is_begin_with_no_accompany(sentence=douhao_sentence):  # 现病史里面的场景
        results[index] = []  # 内容都写到了上一个逗号句子里了
        parse_douhao_sentence_begin_not_accompany(index, douhao_sentence, results)

    else:
        results[index] = parse_general_douhao_sentence(index=index,
                                                       douhao_sentence=douhao_sentence,
                                                       results=results)


def parse_douhao_sentence_begin_not_accompany(index, douhao_sentence, results):
    """
    逗号句子以`不伴`开头：
    e.g. 不伴有气促、头晕，
         不伴有冷汗，
    :param index:
    :param douhao_sentence:
    :param results: 句号句子层面，# {0:[dict,dict], 1:[]}  # 0, 1代表第几个逗号句子
    :return:
    """
    after_sentence = douhao_sentence.split('不##d 伴##v')[-1]
    # 有没有顿号，区分开
    if '、##x' in after_sentence:
        accom_result = parse_dunhao_sentence(douhao_sentence=after_sentence)  # 这里可能提取不到时间
    else:
        accom_result = parse_general_douhao_sentence(index=index, douhao_sentence=after_sentence, results=results)

    # 1. 返回的是个[dict, dict], 要迭代把里面的exist全部改成'无'
    for item in accom_result:
        item['exist'] = '无'

    # 2. 对上一个逗号句子的每一个Symptom添加伴随
    for i in range(index - 1, -1, -1):
        if len(results[i]) == 0:
            continue
        else:
            for item in results[i]:
                if 'accompany' in item.keys() and item['accompany']:
                    item['accompany'].extend(accom_result)
                else:
                    item['accompany'] = accom_result
            break


if __name__ == '__main__':
    print(PROJECT_PATH)
    txt_path = os.path.join(PROJECT_PATH, 'data/data_cur/cur_medical_v2.txt')
    # txt_path = os.path.join(PROJECT_PATH, 'data/test_case/cur_medical_segment_test_cl_0601.txt')

    txt_path = os.path.join(PROJECT_PATH, 'data/bad_case/0603.txt')


    load_txt(txt_path=txt_path)
