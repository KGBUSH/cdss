# -*- coding: utf-8 -*-

"""

@time: 2020/5/28 14:02

@desc: 把主诉那套quick_analyze.py的rules拿过来看看效果



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
from utils.duration import Duration
from utils.extension import Extension
from utils.visualize import View
from utils.grammar import *
from utils.grammar import prog_banjiazhong, prog_zaifa
from utils.pre_processing import *

import os
import re
import numpy as np


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
            if prog_banjiazhong.search(origin) is not None:
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

    elif is_with_scope(sentence=douhao_sentence):
        results[index] = []
        parse_douhao_sentence_with_scope(index, douhao_sentence, results)

    elif is_begin_about_accompany(sentence=douhao_sentence):
        results[index] = []  # 内容都写到了上一个逗号句子里了
        if is_have_negative_word(sentence=douhao_sentence):  # 无伴的情况
            parse_douhao_sentence_begin_not_accompany(index, douhao_sentence, results, exist='无')
        else:
            parse_douhao_sentence_begin_not_accompany(index, douhao_sentence, results)

    elif is_basic_info_status_related_sentence(sentence=douhao_sentence):
        # basicInfo
        results[index] = parse_basic_info_sentence(douhao_sentence=douhao_sentence)

    elif is_totally_useless(sentence=douhao_sentence):
        results[index] = []  # 这句话没有有效词，就空吧

    else:
        results[index] = parse_general_douhao_sentence(index=index,
                                                       douhao_sentence=douhao_sentence,
                                                       results=results)


def parse_douhao_sentence_with_scope(index, douhao_sentence, results):
    """
    处理逗号句子里面有范围的
    ##x 范围##n 约##d 巴##j 掌大##j 小##n
    :param index:
    :param douhao_sentence:
    :param results: 句号句子层面，# {0:[dict,dict], 1:[]}  # 0, 1代表第几个逗号句子
    :return: None
    """
    # 1. 找到 范围后面的内容
    content = douhao_sentence.split('范围##n')[-1]
    origin_content = ''
    for str_ in content.split():
        origin_content += str_.split('##')[0]

    # 2. 找到前面的result且exist不为无
    find_flag = False
    for i in range(index - 1, -1, -1):
        if find_flag:
            break
        if len(results[i]) > 0:  # 这个逗号句子result有东西
            for dict_ in results[i]:
                if dict_['exist'] == '有':
                    find_flag = True
                    dict_['scope'] = origin_content


def parse_douhao_sentence_begin_location(index, douhao_sentence, results):
    """
    逗号句子以`位于`开头：
    e.g. 位于心前区，
    :param index:
    :param douhao_sentence:
    :param results: 句号句子层面，# {0:[dict,dict], 1:[]}  # 0, 1代表第几个逗号句子
    :return: None 结果写入前面的句子result里
    """
    # 1. 找到 Bodypart 是什么
    flag = '##Bodypart'
    after_sentence = douhao_sentence.split('位于##v')[-1].strip()
    body_part_list = []
    for str_ in after_sentence.split():
        if flag in str_:
            body_part_list.append(str_.split(flag)[0])

    len_mark = list(map(len, body_part_list))  # 每个结果的长度， [3, 9]
    select = body_part_list[np.argmax(len_mark)]

    # 2. 放到前面的逗号句子的result中
    for i in range(index - 1, -1, -1):
        if len(results[i]) > 0:  # 这个逗号句子result有东西
            for dict_ in results[i]:
                dict_['part'] = select
            break


def parse_douhao_sentence_begin_not_accompany(index, douhao_sentence, results, exist='有'):
    """
    逗号句子以`不伴`开头：
    e.g. 不伴有气促、头晕，
         不伴有冷汗，
    :param index:
    :param douhao_sentence:
    :param results: 句号句子层面，# {0:[dict,dict], 1:[]}  # 0, 1代表第几个逗号句子
    :param exist: 不伴还是伴
    :return: None 结果写入前面的句子result里
    """
    after_sentence = douhao_sentence.split('伴')[-1].strip()
    # 有没有顿号，区分开
    if '、##x' in after_sentence:
        accom_result = parse_basic_douhao_sentence(douhao_sentence=after_sentence)  # 这里可能提取不到时间
    else:
        accom_result = parse_general_douhao_sentence(index=index, douhao_sentence=after_sentence, results=results)

    # 1. 返回的是个[dict, dict], 要迭代把里面的exist全部改成'无'
    for dict_ in accom_result:
        dict_['exist'] = exist

    # 2. 对上一个逗号句子的每一个Symptom添加伴随
    for i in range(index - 1, -1, -1):
        if len(results[i]) > 0:
            for dict_ in results[i]:
                if 'accompany' in dict_.keys() and dict_['accompany']:
                    dict_['accompany'].extend(accom_result)
                else:
                    dict_['accompany'] = accom_result
            break


def parse_general_douhao_sentence(index, douhao_sentence, results):
    """
    1 先找主实体
    2 再找是否有伴随
    :param douhao_sentence:
    :param results: 句号句子层面，# {0:[dict,dict], 1:[]}  # 0, 1代表第几个逗号句子
    :return: new 了一个句号句子的result[], 返回
    """
    # 1. 先找该逗号句子的主Symptom（可能多个）
    result = []  # [dict, ..., dict]
    duration = Duration.get_duration_re(sentence=douhao_sentence)
    extension = Extension.get_extension(sentence=douhao_sentence)
    accom_before = douhao_sentence.split('伴##x')[0]  # 如果没有'伴##x' 也ok
    # 1.1 找到'伴'前面的主Symptom，可能没有就要往前找
    if '##Symptom' in accom_before or '##Disease' in accom_before:
        result = parse_basic_douhao_sentence(douhao_sentence=accom_before)
        for dict_ in result:
            if not dict_['duration']:
                dict_['duration'] = duration

    else:
        # 这个逗号句子没有Symptom
        try:
            for k in range(len(results[index - 1])):
                symptom = results[index - 1][k]['symptom']  # k 代表之前那句话有多少个Symptom
                tmp = {'symptom': symptom,
                       "target": '自身',
                       'duration': duration}
                tmp.update(extension)
                result.append(tmp)
        except (ValueError, KeyError) as e:
            pass

    # 2. 如果有伴随
    if '伴##x' in douhao_sentence:
        accompany_sentence = douhao_sentence.split('伴##x')[-1]  # 伴后面的内容
        if '##Symptom' in accompany_sentence or \
                '##Disease' in accompany_sentence:  # 伴后面要有主语 才考虑伴随
            # 2.1 解析伴后面的内容
            accom_result = parse_basic_douhao_sentence(douhao_sentence=accompany_sentence)
            # 2.2 加入主Symptom
            for item in result:
                item.update({"accompany": accom_result})

    return result


def parse_basic_douhao_sentence(douhao_sentence):
    """
    处理一般的逗号句子，但是里面可以有顿号。
    一般的逗号句子： 没有伴随、保证句子里至少有一个主体
    :return:  这句逗号句子的多个json
    """
    tmp_result = []  # [dict, dict]
    duration = Duration.get_duration_re(sentence=douhao_sentence)
    extension = Extension.get_extension(sentence=douhao_sentence)
    status = Extension.get_disease_extension(sentence=douhao_sentence)
    for item in douhao_sentence.split(' '):
        if '##Symptom' in item:
            symptom = item.split('##')[0]
            tmp = {"symptom": symptom,
                   "target": '自身',
                   "duration": duration}
            tmp.update(extension)
            tmp_result.append(tmp)

        if '##Disease' in item:
            disease = item.split('##')[0]
            tmp = {"disease": disease,
                   "target": '自身',
                   "status": status,
                   "duration": duration}

            tmp_result.append(tmp)

    return tmp_result


def parse_basic_info_sentence(douhao_sentence):
    """
    前提：必须要有 basicInfo + status
    :param douhao_sentence: 
    :return: 
    """
    tmp_result = []
    status = None
    for str_ in douhao_sentence.split():
        if '##Status' in str_:
            status = str_.split('##Status')[0]
            break

    for str_ in douhao_sentence.split():
        if '##BasicInfo' in str_:
            tmp_result.append({'basicInfo': str_.split('##BasicInfo')[0], 'status': status})
    return tmp_result


if __name__ == '__main__':
    print(PROJECT_PATH)

    # 现病史
    txt_path = os.path.join(PROJECT_PATH, 'data/data_cur/cur_medical_6_4.txt')

    # # 主诉
    # txt_path = os.path.join(PROJECT_PATH, 'data/data_main/chief_complaint_6_4.txt')

    # test_case
    txt_path = os.path.join(PROJECT_PATH, 'data/test_case/0605.txt')

    # bad_case
    # txt_path = os.path.join(PROJECT_PATH, 'data/bad_case/0603.txt')

    load_txt(txt_path=txt_path)
