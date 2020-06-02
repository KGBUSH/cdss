# -*- coding: utf-8 -*-
"""
一些语法判断 func
"""


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
