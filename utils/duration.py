# -*- coding: utf-8 -*-
import re

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

prog = re.compile('([一二三四五六七八九十]|(([0-9]*)\.)?([0-9]*)(\+|余)?|半|多)?(个)?(月|天|小时|年|周|次)(半|余)?')


class Duration(object):

    @staticmethod
    def get_duration_re(sentence):
        words = sentence.split()
        s = ''
        for word in words:
            s += word.split('##')[0]
        duration = prog.search(s[:])
        if duration is not None:
            duration = duration.group()
            if '余' in duration:
                idx = duration.index('余')
                duration = duration[:idx] + duration[idx + 1:] + '+'
        return duration

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
