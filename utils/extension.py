
import re

"""
提取维度词 ext_*
"""

# 类似1次，算作频率
prog_ci = re.compile('([一二三四五六七八九十]*|([0-9]*)?(-[0-9]*)?|多)?(次)')
prog_status = re.compile('[考虑|拟|我科|住院|诊断|入院|]')


class Extension(object):

    @staticmethod
    def get_extension(sentence):  # TODO 应该把accompany加上

        invalid = ''
        intensity = sentence.split('##ext_intensity')[0].split()[-1] if '##ext_intensity' in sentence else invalid
        part = sentence.split('##Bodypart')[0].split()[-1] if '##Bodypart' in sentence else invalid
        exist = _get_exist(sentence, invalid)

        frequency = _get_frequency(sentence, invalid)

        color = sentence.split('##ext_color')[0].split()[-1] if '##ext_color' in sentence else invalid  # 颜色
        property_ = invalid  # 触感
        premise = sentence.split('##ext_premise')[0].split()[-1] if '##ext_premise' in sentence else invalid

        scope = invalid  # 范围
        smell = invalid  # 味道

        return {'intensity': intensity,
                'part': part,
                'exist': exist,
                'frequency': frequency,
                'color': color,
                'property': property_,
                'premise': premise,
                'scope': scope,
                'smell': smell}

    @staticmethod
    def get_disease_extension(sentence):
        """
        考虑 + disease
        拟 + disease + 收入我科
        disease + 入住我科
        以 + d + 收住院
        d + 收住院
        以 + d + 收住我科
        诊断为 + d + 转入我科
        诊断 + d
        以 + d + 收入院
        :param sentence:
        :return:
        """
        if '##Disease' not in sentence:
            return ''
        idx = prog_status.search(sentence)
        if idx:
            return '入院原因'


def _get_frequency(sentence, invalid):

    frequency = sentence.split('##ext_freq')[0].split()[-1] if '##ext_freq' in sentence else invalid
    words = sentence.split()
    s = ''
    for word in words:
        s += word.split('##')[0]
    freq = prog_ci.search(s[:])
    if freq is not None:
        freq = freq.group()
        return frequency + freq
    else:
        return frequency


def _get_exist(sentence, invalid):

    exist = '无' if "无##" in sentence else '有'
    words = sentence.split()
    s = ''
    for word in words:
        s += word.split('##')[0]
    if '无明显诱因' in s:
        exist = '有'
    return exist
