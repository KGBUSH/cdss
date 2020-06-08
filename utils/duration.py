# -*- coding: utf-8 -*-
import re

"""
duration提取
"""

time_nomalize = {
    '天': 24,
    '周': 7 * 24,
    '月': 30 * 7 * 24,
    '年': 12 * 30 * 7 * 24
}

digit_dict = {"零": 0, "一": 1, "二": 2, "两": 2, "俩": 2, "三": 3,
              "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}

prog = re.compile('(近|约)?([一二三四五六七八九十]|(([0-9]*)\.)?([0-9]*)(\+|余)?|半|多|数)?(个)?(月|天|小时|年|周|分钟)(半|余)?')


class Duration(object):

    @staticmethod
    def get_duration_re(sentence):
        """
        如果没有duration 返回None
        :param sentence:
        :return:
        """
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
    def normalize_time(duration):
        """
        统一为小时h
        :param duration: get_duration_re 中提取出来的duration
        :return:
        """
        for key in time_nomalize.keys():
            if key in duration:
                tmp_list = duration.split(key)
                num = -1
                try:
                    num = int(tmp_list[0])
                except ValueError:
                    try:
                        num = digit_dict[tmp_list[0]]
                    except:
                        raise ValueError
                num *= time_nomalize[key]
                num = str(num)  # 最后再转回str
                if tmp_list[-1] == '+':
                    num += '+'
                return num

