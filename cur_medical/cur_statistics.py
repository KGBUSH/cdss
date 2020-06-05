# -*- coding: utf-8 -*-

"""

@file: cur_statistics.py

@time: 2020/5/28 14:52

@desc: 统计
1 `现病史`中有多少分词实体被识别出来了， 目前跑下来结果是
2 哪些是目前的`无用`词


@todo: 这个统计recall的方法还是不够准
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


if __name__ == '__main__':
    print(PROJECT_PATH)
    txt_path = os.path.join(PROJECT_PATH, 'data/data_cur/cur_medical_6_4.txt')
    # txt_path = os.path.join(PROJECT_PATH, 'data/test_case_cl.txt')

    # statistics_efficient_percent(txt_path=txt_path)

    # 钟博的那种格式
    from chief_complaint.main_statistics import statistics_efficient_percent_format

    statistics_efficient_percent_format(txt_path=txt_path)
