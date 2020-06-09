
import re

"""
提取维度词 ext_*
"""

# 类似1次，算作频率
prog_ci = re.compile('([一二三四五六七八九十]*|([0-9]*)?(-[0-9]*)?|多)?(次)')


class Extension(object):

    @staticmethod
    def get_extension(sentence):  # TODO 应该把accompany加上

        invalid = ''
        intensity = sentence.split('##ext_intensity')[0].split()[-1] if '##ext_intensity' in sentence else invalid
        part = sentence.split('##Bodypart')[0].split()[-1] if '##Bodypart' in sentence else invalid
        exist = '无' if '无##x' in sentence else '有'
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
