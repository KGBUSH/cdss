# -*- coding: utf-8 -*-

"""

@file: parse.py

@time: 2020/6/11 14:55

@desc: 每条规则的解析细节实现

"""

from utils.duration import Duration
from utils.extension import Extension

import numpy as np


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


def parse_douhao_sentence_about_accompany(index, douhao_sentence, results, exist='有'):
    """
    逗号句子是关于伴或者不伴的：
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

    # 1. 找到status
    status = None
    for str_ in douhao_sentence.split():
        if '##Status' in str_:
            status = str_.split('##Status')[0]
            break
    # 2. 组装
    for str_ in douhao_sentence.split():
        if '##BasicInfo' in str_:
            tmp_result.append({'basicInfo': str_.split('##BasicInfo')[0], 'status': status})
    return tmp_result

