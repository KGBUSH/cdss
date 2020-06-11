## 总入口

rule_analyze_v1.py

同时可支持主诉和现病史两种类型的文本。

**运行**
    
    1. txt_path 赋值要解析的文件
    2. run()  按行解析





## 目录结构说明

/data: 数据。包含现病史，主诉，以及testcase

/chief_complaint：主诉相关代码，目前只有statistics

/cur_medical：现病史相关代码，目前只有statistics

/utils 工具包

1. duration.py  时间相关
2. extension.py  维度
3. grammar.py  语法判断
4. pre_processing.py  预处理
5. visualize.py  打印


