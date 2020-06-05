# -*- coding: utf-8 -*-

"""

@file: main_statistics.py

@time: 2020/5/28 14:52

@desc: 统计
1 `主诉`中有多少分词实体被识别出来了， 目前跑下来结果是80%
2 哪些是目前的`无用`词

"""

from config import PROJECT_PATH
import os
from rule_analyze_v1 import parse_one_input

from collections import Counter


def count_total_cut_word(input):
    """
    计算这个case 分词中有多少词， 按## 分割
    :param input:
    :return:
    """
    count = input.count('##')
    count -= input.count('##x')
    return count


def count_valid_from_results(results):
    """
    看results 里面有多少维度
    :param results:
    :return:
    """
    count_valid = 0
    for k, item in enumerate(results):  # 句号句子
        for key, value in item.items():
            for d in value:  # 逗号句子
                for v in d.values():
                    if v and v != '自身' and v != '有':
                        count_valid += 1
    return count_valid


def update_useless_word(l, all_results, input):
    """
    把无用的词添加到l中
    :param l: list, 所有useless的词都添加进来
    :param all_results: 一整段话的results
    :param input: input，杜博分词后的结果
    :return:
    """
    tmp_all_results = str(all_results)
    for cut in input.split():
        if cut.split('##')[0] not in tmp_all_results:
            l.append(cut)
            if cut == '心悸##Symptom':
                aaa = 1


def statistics_efficient_percent(txt_path):
    """
    e.g. /Users/dengyang/PycharmProjects/cdss/data/main_complaint_segment.txt
    统计有多少分词在省城json时
    """
    # 1. 按行load文件
    lines_num = -1
    with open(txt_path, 'r', encoding='utf-8') as fr:
        lines_num = len(fr.readlines())

    sample_f = open(txt_path, 'r', encoding='utf-8')
    print("load samples from %s ... ..." % txt_path)

    count_cut_word = 0
    count_valid = 0
    list_useless = []

    for i in range(int(lines_num)):
        line = sample_f.readline()
        line = line.strip('\n').strip()
        line = line.replace(',', '，')
        if line == '':
            continue
        try:
            origin, input = line.split('\t')[0], line.split('\t')[-1]  # 真正的input是分好词的，（line的后面一部分）
            all_results = parse_one_input(input=input)
            print(origin, '\n\t', all_results)

            count_cut_word += count_total_cut_word(input)
            count_valid += count_valid_from_results(all_results)
            update_useless_word(l=list_useless, all_results=all_results, input=input)

        except:
            pass
    print('汇总：', count_cut_word, count_valid, float(count_valid) / count_cut_word)
    counter_useless = Counter(list_useless).most_common()
    # print(counter_useless)
    for i, item in enumerate(counter_useless):
        print(i, item)


def statistics_efficient_percent_format(txt_path):
    """
    按钟博的输出格式：
    反复## 胸闷## 1周，## 加重## 9小时。##   =======  胸闷##, 加重##  =======   5  =======   2  ======= 40 %
    第一列为杜总分好词的结果，第二列为你识别到的结果，第三列是这句主诉分词完的个数，第四列是识别到的个数，第5列是前两列相除。

    e.g. /Users/dengyang/PycharmProjects/cdss/data/main_complaint_segment.txt
    统计有多少分词在省城json时
    """
    # 1. 按行load文件
    lines_num = -1
    with open(txt_path, 'r', encoding='utf-8') as fr:
        lines_num = len(fr.readlines())

    sample_f = open(txt_path, 'r', encoding='utf-8')
    print("load samples from %s ... ..." % txt_path)

    count_cut_word = 0
    count_valid = 0
    list_useless = []

    for i in range(int(lines_num)):
        line = sample_f.readline()
        line = line.strip('\n').strip()
        line = line.replace(',', '，')
        if line == '':
            continue
        try:
            origin, input = line.split('\t')[0], line.split('\t')[-1]  # 真正的input是分好词的，（line的后面一部分）
            all_results = parse_one_input(input=input)
            # print(origin, '\n\t', all_results)

            str_all_results = str(all_results)

            # 第二列
            col2 = ''  # 第二列内容
            col4 = 0  # 有效词个数
            for str_ in input.split(' '):
                word = str_.split('##')[0]
                if word in str_all_results:
                    col4 += 1
                    col2 += str_
                    col2 += ' '

            # 第三列 总个数
            col3 = count_total_cut_word(input)

            # 第五列 percent
            col5 = float(col4) / col3

            # 组装
            out_print = ''
            p = '\t'
            out_print += input + p
            out_print += col2 + p
            out_print += str(col3) + p
            out_print += str(col4) + p
            out_print += str(col5 * 100) + '%'
            print(out_print)

            count_cut_word += col3  # 这段话总词个数
            count_valid += col4  # 有效词个数
        except:
            pass
    print('汇总：', count_cut_word, count_valid, float(count_valid) / count_cut_word)


if __name__ == '__main__':
    print(PROJECT_PATH)
    txt_path = os.path.join(PROJECT_PATH, 'data/data_main/main_complaint_v2.txt')
    # txt_path = os.path.join(PROJECT_PATH, 'data/test_case_cl.txt')

    # statistics_efficient_percent(txt_path=txt_path)
    statistics_efficient_percent_format(txt_path=txt_path)
