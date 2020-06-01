# -*- coding: utf-8 -*-


def print_paragraph_result(paragraph_list):
    for i, juzi_result in enumerate(paragraph_list):
        print('第%d个逗号句子' % i)
        tab = '\t'
        for index in juzi_result.keys():
            print(tab + '第%d个逗号句子' % index)
            for item in juzi_result[index]:
                print(tab * 2 + str(item))
                if 'accompany' in item.keys() and item['accompany']:
                    for accom in item['accompany']:
                        print(tab * 3 + str(accom))

    print('\n')

