# -*- coding: utf-8 -*-

"""
调试jieba
"""

import jieba
import pkuseg

seg = pkuseg.pkuseg()           # 以默认配置加载模型
text = seg.cut('我爱阿莫西林')  # 进行分词
print(text)



seg = pkuseg.pkuseg(model_name='medicine')  # 程序会自动下载所对应的细领域模型
text = seg.cut('我爱阿莫西林')              # 进行分词
print(text)


seg = pkuseg.pkuseg(postag=True)  # 开启词性标注功能
text = seg.cut('我爱北京天安门，我爱阿莫西林')    # 进行分词和词性标注
print(text)