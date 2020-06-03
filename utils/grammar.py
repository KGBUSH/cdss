# -*- coding: utf-8 -*-
"""
一些语法判断 func
"""
from utils.duration import Duration


def is_begin_with_no_accompany(sentence):
    """
    e.g. 无伴出汗、胸闷、气促，
    :param sentence:
    :return:
    """
    if sentence.strip().startswith('不##d 伴##v') \
            or sentence.strip().startswith('无##d 伴##v') \
            or sentence.strip().startswith('无伴##v') \
            or sentence.strip().startswith('不伴##v'):
        return True
    return False


def is_totally_useless(sentence):
    """
    什么有效信息都没有，（目前只考虑Symptom，Disease，还有duration，duration要自己去提取）
    :param sentence:
    :return:
    """
    duration = Duration.get_duration_re(sentence=sentence)

    if 'Symptom' not in sentence \
            and 'Disease' not in sentence\
            and not duration:
        return True
    else:
        return False
