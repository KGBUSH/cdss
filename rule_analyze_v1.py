# -*- coding: utf-8 -*-

"""

@time: 2020/5/28 14:02

@desc: rules解析主程序



input的原句：腹胀、纳差4天，胸闷1天
input: 腹胀##Symptom 、##x 纳差##Symptom 4##m 天##n ，##x 胸闷##Symptom 1##m 天##n
output:
{"symptom" : '腹胀', "target" : '自身', "duration" : '4天', "intensity" : '', "part" : '', "exist" : '有', "frequency" : '', "color" : '',
    "property" : '', "pattern" : '', "type" : '', "scope" : '', "smell" : '', "accompany" : '',  "premise" : ''}
{"symptom" : '纳差', "target" : '自身', "duration" : '4天', "intensity" : '', "part" : '', "exist" : '有', "frequency" : '', "color" : '',
    "property" : '', "pattern" : '', "type" : '', "scope" : '', "smell" : '', "accompany" : ',  "premise" : '''}
{"symptom" : '胸闷', "target" : '自身', "duration" : '1天', "intensity" : '', "part" : '', "exist" : '有', "frequency" : '', "color" : '',
    "property" : '', "pattern" : '', "type" : '', "scope" : '', "smell" : '', "accompany" : '',  "premise" : ''}




发现血压升高5年，血压控制不稳伴活动后气促2月。
发现##v 血压升高##Symptom 5##m 年##m ，##x 血压##Labindex 控制##v 不稳##a 伴##v 活动后##ext_premise 气促##Symptom 2##m 月##m 。##x
{"symptom" : '血压升高', "duration" : '5年', "intensity" : '', "part" : '', "exist" : '有', "frequency" : '', "color" : '',
    "property" : '', "pattern" : '', "type" : '', "scope" : '', "smell" : '', "accompany" : '',  "premise" : ''}
{"symptom" : '血压控制不稳', "target" : '自身', "duration" : '2月', "intensity" : '', "part" : '', "exist" : '有', "frequency" : '', "color" : '',
    "property" : '', "pattern" : '', "type" : '', "scope" : '', "smell" : '',
    "accompany" :
        '{"symptom" : '活动后气促', "target" : '自身', "duration" : '2月', "intensity" : '', "part" : '', "exist" : '有', "frequency" : '', "color" : '',
        "property" : '', "pattern" : '', "type" : '', "scope" : '', "smell" : '', "accompany" : '',  "premise" : ''}',  "premise" : ''}


"""

from config import PROJECT_PATH
from utils.visualize import View
from utils.grammar import *
from utils.grammar import prog_banjiazhong, prog_zaifa
from utils.pre_processing import *
from utils.parse import *

import os


def run(txt_path):
    """
    e.g. /Users/dengyang/PycharmProjects/cdss/data/main_complaint_segment.txt
    """
    # 1. 按行load文件
    lines_num = -1
    with open(txt_path, 'r', encoding='utf-8') as fr:
        lines_num = len(fr.readlines())

    fr = open(txt_path, 'r', encoding='utf-8')
    print("load samples from %s ... ..." % txt_path)
    for i in range(int(lines_num)):
        line = fr.readline()
        line = pre_for_paragraph(line)
        if line == '':
            continue
        try:
            origin, input = line.split('\t')[0], line.split('\t')[-1]  # 真正的input是分好词的，（line的后面一部分）
            if prog_banjiazhong.search(origin) is not None:  # TODO 这个应该放到逗号句子总入口那里做规则前的pre_processing
                input = input.replace('加重##ext_intensity', '，##x 加重##ext_intensity')
            all_results = parse_one_input(input=input)

            View.visualize(origin, input, all_results, mode='non-void')
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
            parse_douhao_sentence_entrance(index=i, douhao_sentence=douhao_sentence, results=results)
        all_results.append(results)
    return all_results


def parse_douhao_sentence_entrance(index, douhao_sentence, results):
    """
    逗号句子总入口
    :param index: 这是这个句号句子里面的第几个逗号句子
    :param douhao_sentence: 逗号句子
    :param results: 句号句子层面，# {0:[dict,dict], 1:[]}  # 0, 1代表第几个逗号句子
    :return:
    """
    # 1. 针对逗号句子的预处理
    douhao_sentence = conbine_similar_terms(input=douhao_sentence)
    douhao_sentence = pre_for_basic_info_status(douhao_sentence=douhao_sentence)
    douhao_sentence = pre_for_zaifa(douhao_sentence=douhao_sentence)

    # 2. rules总入口
    if is_begin_with_location(sentence=douhao_sentence):  # "，位于心前区，"
        results[index] = []
        parse_douhao_sentence_begin_location(index, douhao_sentence, results)

    elif is_begin_with_keep_time(sentence=douhao_sentence):
        results[index] = []
        parse_douhao_sentence_with_keep_time(index, douhao_sentence, results)

    elif is_with_scope(sentence=douhao_sentence):
        results[index] = []
        parse_douhao_sentence_with_scope(index, douhao_sentence, results)

    elif is_begin_about_accompany(sentence=douhao_sentence):
        results[index] = []  # 内容都写到了上一个逗号句子里了
        if is_have_negative_word(sentence=douhao_sentence):  # 无伴的情况
            parse_douhao_sentence_about_accompany(index, douhao_sentence, results, exist='无')
        else:
            parse_douhao_sentence_about_accompany(index, douhao_sentence, results)

    elif is_basic_info_status_related_sentence(sentence=douhao_sentence):
        # basicInfo
        results[index] = parse_basic_info_sentence(douhao_sentence=douhao_sentence)

    elif is_totally_useless(sentence=douhao_sentence):
        results[index] = []  # 这句话没有有效词，就空吧

    else:
        results[index] = parse_general_douhao_sentence(index=index,
                                                       douhao_sentence=douhao_sentence,
                                                       results=results)


if __name__ == '__main__':
    print(PROJECT_PATH)

    # 现病史
    # txt_path = os.path.join(PROJECT_PATH, 'data/data_cur/cur_medical_6_4.txt')

    # # 主诉
    # txt_path = os.path.join(PROJECT_PATH, 'data/data_main/chief_complaint_6_4.txt')

    # test_case
    txt_path = os.path.join(PROJECT_PATH, 'data/test_case/0605.txt')

    # bad_case
    # txt_path = os.path.join(PROJECT_PATH, 'data/bad_case/0603.txt')

    run(txt_path=txt_path)
