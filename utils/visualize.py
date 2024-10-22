class View:

    @staticmethod
    def visualize(origin, input, results, mode='full'):
        """
        使用缩进等，便于展示维度提取结果。
        :param origin: 原始句子
        :param input
        :param results: 维度提取结果 [dict, dict]
        :param mode: full时展示所有维度
                     non-void时仅显示非空的维度
        """
        # 1. 打印原始句子
        print("##### 原始句子：")
        origin_list = origin.split('。')
        for i, str_ in enumerate(origin_list):
            print('\t', '第%d句: ' % i, str_)

        # 2. 打印分词结果
        print("##### 分词结果：")
        input_list = input.strip().strip('。##x').split('。##x')  # 先把最后的句号删了，再split by 句号
        for i, str_ in enumerate(input_list):
            print('\t', '第%d句: ' % i, str_)

        # 3. 打印维度提取词
        print("##### 维度提取结果：")
        for i, dict_ in enumerate(results):
            print('第%d个句号句子' % i)
            print(origin_list[i])
            print(input_list[i])
            for key, value in dict_.items():
                print('  第%d:%d个逗号句子' % (i, key))
                parse_decode_value(value, mode=mode)
        print('\n\n\n')


def parse_decode_value(value, mode='full'):
    if mode == 'full':
        for dict_ in value:
            if 'accompany' not in dict_:
                print("\t", dict_)
            else:
                temp_dict_ = dict_.copy()
                temp_dict_['accompany'] = '有'
                print("\t", temp_dict_)
                print("\t", "accompany:")
                for dict__ in dict_['accompany']:
                    print("\t\t", dict__)
    elif mode == 'non-void':
        for dict_ in value:
            if 'accompany' not in dict_:
                temp_dict_for_print = {k: v for k, v in dict_.items() if v != ''}
                print("\t", temp_dict_for_print)
            else:
                temp_dict_ = dict_.copy()
                temp_dict_['accompany'] = '有'
                temp_dict_for_print = {k: v for k, v in temp_dict_.items() if v != ''}
                print("\t", temp_dict_for_print)
                print("\t", "accompany:")
                for dict__ in dict_['accompany']:
                    temp_dict_for_print = {k: v for k, v in dict__.items() if v != ''}
                    print("\t\t", temp_dict_for_print)


origin = '四肢乏力伴精神行为异常1天。'
results = [{0: [{'symptom': '乏力', 'target': '自身', 'duration': '1天', 'intensity': '', 'part': '四肢', 'exist': '有',
                 'frequency': '', 'color': '', 'property': '', 'premise': '', 'scope': '', 'smell': '',
                 'accompany': [{'symptom': '乏力', 'duration': '1天', 'intensity': '', 'part': '', 'exist': '有',
                                'frequency': '', 'color': '', 'property': '', 'premise': '', 'scope': '', 'smell': ''}]
                 }]}]

if __name__ == '__main__':
    View.visualize(origin, results, mode='non-void')
