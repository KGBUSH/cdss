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

#import jieba
import os
import collections
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
        if line == '':
            continue
        try:
            # line = '反复胸闷10余年,再发1月。\t反复##ext_freq 胸闷##Symptom 10##m 余年##m ,##x 再发##ext_freq 1##m 月##m 。##x'
            # line = '腹胀、纳差4天，胸闷1天\t腹胀##Symptom 、##x 纳差##Symptom 4##m 天##n ，##x 胸闷##Symptom 1##m 天##n'
            origin, input = line.split('\t')[0], line.split('\t')[-1]  # 真正的input是分好词的，（line的后面一部分）
            results = parse_one_input(input=input)
            print(origin, results)
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
    input_list = input.strip('。##x').split('。##x')  # 先把最后的句号删了，再split by 句号

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

    :param douhao_sentence: 逗号句子
    :return:
    """
    # 1. 有顿号的逗号句子（一定有多个Symptom）
    if '、##x' in douhao_sentence:
        results[index] = parse_dunhao_sentence(douhao_sentence=douhao_sentence)

    # 2. 陈磊负责没有顿号
    elif '##Symptom' in douhao_sentence:
        # 没有顿号的情况下，应该只有一个症状
        words = douhao_sentence.split('##Symptom')
        symptom = words[0].split()[-1]
        duration = Duration.get_duration_re(sentence=words[1])
        results[index] = [{'symptom': symptom, 'duration': duration}]
    else:
        # 这个逗号句子没有Symptom
        symptom = None
        for j in range(index - 1, -1, -1):
            symptom = results[j][-1]['symptom']
        duration = Duration.get_duration_re(sentence=douhao_sentence)
        results[index] = [{'symptom': symptom, 'duration': duration}]


def parse_dunhao_sentence(douhao_sentence):
    """
    有`顿号`的逗号句子里面默认应该是有Symptom的
    且至少两个Symptom
    :return:  这句逗号句子的多个json
    """
    tmp_result = []  # [dict, dict]
    s_count = douhao_sentence.count('##Symptom')
    duration = Duration.get_duration_re(sentence=douhao_sentence)
    for item in douhao_sentence.split(' '):
        if '##Symptom' in item:
            symptom = item.split('##')[0]
            tmp_result.append({"symptom": symptom,
                               "target": '自身',
                               "duration": duration})
    return tmp_result


if __name__ == '__main__':
    print("test")
    print(PROJECT_PATH)
    txt_path = os.path.join(PROJECT_PATH, 'data/main_complaint_segment.txt')
    load_txt(txt_path=txt_path)
