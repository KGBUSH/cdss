
import re

"""
提取维度词 ext_*
"""


class Extension(object):

    @staticmethod
    def get_extension(sentence):

        invalid = ''
        intensity = sentence.split('##ext_intensity')[0].split()[-1] if '##ext_intensity' in sentence else invalid
        part = sentence.split('##Bodypart')[0].split()[-1] if '##Bodypart' in sentence else invalid
        exist = '有'
        frequency = sentence.split('##ext_freq')[0].split()[-1] if '##ext_freq' in sentence else invalid
        color = invalid  # 颜色
        property_ = invalid  # 触感
        pattern = invalid
        type_ = invalid  # 病理
        scope = invalid  # 范围
        smell = invalid  # 味道

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
