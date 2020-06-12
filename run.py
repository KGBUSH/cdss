# -*- coding: utf-8 -*-

"""

@time: 2020/6/12 12:07

@desc: 命令行执行

"""
from config import PROJECT_PATH
import rule_analyze_v1
import argparse


def run():
    parser = argparse.ArgumentParser(description='cdss rules')
    parser.add_argument("--txt_path", type=str, default=0)
    args = parser.parse_args()
    txt_path = args.txt_path

    print(PROJECT_PATH)
    rule_analyze_v1.main(txt_path=txt_path)


if __name__ == '__main__':
    """
    运行命令 example 
    python run.py  --txt_path=data/test_case/0605.txt
    """
    run()
