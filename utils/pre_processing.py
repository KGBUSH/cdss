# -*- coding: utf-8 -*-


def pre_for_basic_info_status(douhao_sentence):
    """

    :param douhao_sentence:
    :return:
    """
    # 精神##BasicInfo 可##x -> 这种情况下吧##x替换成##Status
    douhao_sentence = douhao_sentence.replace('BasicInfo 可##x', 'BasicInfo 可##Status')

    return douhao_sentence
