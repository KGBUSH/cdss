# 总入口

**rule_analyze_v1.py  一键运行**

同时可支持主诉和现病史两种类型的文本。

**步骤**
    
    1. txt_path 赋值要解析的文件
    2. run()  按行解析





# 目录结构说明

/data: 数据。包含现病史，主诉，以及testcase

/chief_complaint：主诉相关代码，目前只有statistics

/cur_medical：现病史相关代码，目前只有statistics

/utils 工具包

1. duration.py  _时间相关_
2. extension.py  _维度_
3. grammar.py  _语法判断_
4. pre_processing.py  _预处理_
5. visualize.py  _打印_
6. parse.py  _rules实现细节_



# 备注
**rules的思维导图**在 document/思维导图cdss-0611.emmx。打开浏览器 [链接](https://mm.edrawsoft.cn/files)，然后导入：


![image](http://note.youdao.com/yws/res/17000/C5A2C9A65FE1458D824B4E11BBB4749C)