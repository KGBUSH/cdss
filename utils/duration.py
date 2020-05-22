# -*- coding: utf-8 -*-

"""
duration提取
"""
duration_rules = {
    '##m 余年##m': '余年',
    '##m 年##m 余##m': '年余',
    '##m 年##m': '年',
    '半年##m': '半年',

    '##m 月##m': '月',
    '##m 周##nr': '周',
    '##m 天##n': '天',
    '##m 小##a 时##ng': '小时'
}


class Duration(object):

    @staticmethod
    def get_duration(sentence):
        """
        v1.0 版本获取时间
        :param sentence:
        :return:
        """
        flag = None
        for key in duration_rules.keys():
            if key in sentence:
                flag = key
                break
        if flag is None:
            return ''

        # 如果能找到
        if flag == '半年##m':
            return '半年'
        num = sentence.split(flag)[0].split(' ')[-1]  # 拿到数字
        return str(num) + duration_rules[flag]
