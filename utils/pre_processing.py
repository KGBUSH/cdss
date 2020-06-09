# -*- coding: utf-8 -*-
from utils.grammar import prog_zaifa
from utils.duration import Duration


def pre_for_basic_info_status(douhao_sentence):
    """
    精神##BasicInfo 可##x -> 这种情况下吧##x替换成##Status
    :param douhao_sentence:
    :return:
    """
    douhao_sentence = douhao_sentence.replace('BasicInfo 可##x', 'BasicInfo 可##Status')
    return douhao_sentence


def pre_for_zaifa(douhao_sentence):
    """
    再发前面到底加不加逗号
    胸闷、气促17年再发加重1月余。
    :param douhao_sentence:
    :return:
    """
    cut_flag = True
    if prog_zaifa.search(douhao_sentence):
        tmp_list = douhao_sentence.split('再发')
        for str_ in tmp_list:
            duration = Duration.get_duration_re(sentence=douhao_sentence)
            if not duration:
                cut_flag = False  # 只要前后有一个分句没有duration就不能cut

    if cut_flag:
        douhao_sentence = douhao_sentence.replace('再发##ext_freq', '，##x 再发##ext_freq')
    return douhao_sentence