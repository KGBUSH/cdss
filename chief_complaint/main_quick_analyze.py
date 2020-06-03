"""
@time: 2020/5/22 13:10
@desc: 快速迭代

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
    # 1. 有顿号的逗号句子（一定有多个Symptom）
    # if '、##x' in douhao_sentence and '伴##x' not in douhao_sentence:
    #     results[index] = parse_dunhao_sentence(douhao_sentence=douhao_sentence)
    if False:
        pass

    # 2. 没有顿号
    else:
        results[index] = parse_general_douhao_sentence(index=index,
                                                       douhao_sentence=douhao_sentence,
                                                       results=results)


def parse_general_douhao_sentence(index, douhao_sentence, results):
    """
    1）有伴随
    2）无伴随
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
        # # 没有顿号的情况下，应该只有一个症状
        # words = accom_before.split('##Symptom')
        # symptom = words[0].split()[-1]
        # tmp = {'symptom': symptom,
        #        "target": '自身',
        #        'duration': duration}
        # tmp.update(extension)
        # result.append(tmp)  # TODO 要改

        result = parse_dunhao_sentence(douhao_sentence=accom_before)
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
        # 2.1 解析伴后面的内容，
        accompany_sentence = douhao_sentence.split('伴##x')[-1]  # 伴后面的内容
        if '##Symptom' in accompany_sentence:  # 伴后面要有symptom 才考虑伴随
            extension = Extension.get_extension(sentence=accompany_sentence)
            accom_result = []
            if '、##x' in accompany_sentence or accompany_sentence.count('##Symptom') > 1:
                # 伴随症状至少两个
                accom_result = parse_dunhao_sentence(douhao_sentence=accompany_sentence)
            else:
                # 只有一个伴随症状
                words = accompany_sentence.split('##Symptom')
                symptom = words[0].split()[-1]
                tmp = {'symptom': symptom, 'duration': duration}
                tmp.update(extension)
                accom_result.append(tmp)
            # 2.2 加入主Symptom
            for item in result:
                item.update({"accompany": accom_result})

    return result


def parse_dunhao_sentence(douhao_sentence):
    """
    有`顿号`的逗号句子里面默认应该是有Symptom的
    且至少两个Symptom
    :return:  这句逗号句子的多个json
    """
    tmp_result = []  # [dict, dict]
    s_count = douhao_sentence.count('##Symptom')
    duration = Duration.get_duration_re(sentence=douhao_sentence)
    extension = Extension.get_extension(sentence=douhao_sentence)
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
                   "duration": duration}
            tmp_result.append(tmp)

    return tmp_result


if __name__ == '__main__':
    print(PROJECT_PATH)

    txt_path = os.path.join(PROJECT_PATH, 'data/bad_case/0603.txt')
    # txt_path = os.path.join(PROJECT_PATH, 'data/test_case_cl.txt')

    # txt_path = os.path.join(PROJECT_PATH, 'data/test_case_cl.txt')

    load_txt(txt_path=txt_path)
