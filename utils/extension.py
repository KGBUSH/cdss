# -*- coding: utf-8 -*-
import re

"""
提取维度词 ext_*
"""


class Extension(object):

    @staticmethod
    def get_extension(sentence):

        intensity = sentence.split('##ext_intensity')[0].split()[-1] if '##ext_intensity' in sentence else ' '
        part = sentence.split('##Bodypart')[0].split()[-1] if '##Bodypart' in sentence else ' '
        exist = '有'
        frequency = sentence.split('##ext_freq')[0].split()[-1] if '##ext_freq' in sentence else ' '
        color = ' '  # 颜色
        property_ = ' '  # 触感
        pattern = ' '
        type_ = ' '  # 病理
        scope = ' '  # 范围
        smell = ' '  # 味道

        return {'intensity': intensity,
                'part': part,
                'exist': exist,
                'frequency': frequency,
                'color': color,
                'property': property_,
                'pattern': pattern,
                'type': type_,
                'scope': scope,
                'smell': smell}
