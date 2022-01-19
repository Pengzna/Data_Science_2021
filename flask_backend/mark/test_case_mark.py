'''
本程序用于对hanlp模型进行评估，需要在目录res下存放用于测试的txt和json，直接运行
'''

import os
import json
import hanlp
import sys
import json
import operator
HanLP = hanlp.load(
    hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH, task=["tok/fine"])  # 世界最大中文语料库
tasks = list(HanLP.tasks.keys())
for task in tasks:  # 缩减任务
    if task not in ('tok/fine', 'pos/pku', 'srl', 'ner/pku', 'ner/ontonotes'):
        del HanLP[task]
case_text = ''
stw = []
# 加载停词表
with open('my_stopwords.txt', 'r', encoding='utf-8') as f:
    stw = f.read().split('\n')
tokDate = {}
marks = {}
marks['当事人'] = []
marks['性别'] = []
marks['民族'] = []
marks['出生地'] = []
marks['案由'] = []
marks['相关法院'] = []
# 词性
marks['名词'] = []
marks['动词'] = []
marks['形容词'] = []
marks['副词'] = []


def tok(content):  # 字符串
    global tokDate
    tokDate = json.loads(str(HanLP(content)))  # dict


def mark():
    # 避免出现被告人简述不在第2个的情况
    line = 2
    while("男" not in case_text.split('\n')[line] and "女" not in case_text.split('\n')[line]):
        line = line + 1
    for item in case_text.split('\n')[line].split('，'):
        if('出生于' in item):
            marks['出生地'].append(item[item.index('于')+1:])
        elif(item.endswith('族')):
            marks['民族'].append(item)
        elif(item == '男' or item == '女'):
            marks['性别'].append(item)
        elif('被告人' in item):
            marks['当事人'].append(item.replace('\u3000\u3000被告人', ''))

    for item in tokDate['ner/pku']:
        if(item[1] == 'nt' and '法院' in item[0]):
            marks['相关法院'].append(item[0])
    for item in tokDate['srl']:
        if('出生地' in item[0][0]):
            marks['出生地'].append(item[0][0].replace('出生地', ''))
        else:
            for i in range(0, len(item)):
                if(item[i][0] == '犯'):
                    for word in item:
                        if('罪' in word[0]):
                            marks['案由'].append(word[0])
                elif('犯' in item[i][0] and '罪' in item[i][0] and len(item[i][0]) < 20):
                    marks['案由'].append(
                        item[i][0][item[i][0].index('犯')+1: item[i][0].index('罪')])

    for item, pos in zip(tokDate['tok/fine'], tokDate['pos/pku']):
        if(item not in stw):  # 排除停词表中的无意义词
            if(pos in ['nr', 'ns', 'nt', 'nz']):
                marks['名词'].append(item)
            elif(pos in ['v'] and len(item) > 1):
                marks['动词'].append(item)
            elif(pos == 'a'):
                marks['形容词'].append(item)
            elif(pos in ['ad', 'd']):
                marks['副词'].append(item)

    # 进一步处理
    # 取姓名中出现频率最高的
    marks['性别'] = [marks['性别'][0]]
    # 取民族中的第一项
    marks['民族'] = [marks['民族'][0]]
    # 取出生地中完整的信息，删除带标点的
    for item in marks['出生地']:
        if('，' in item):
            marks['出生地'].remove(item)
    # 案由中不包含"罪"
    for i in range(0, len(marks['案由'])):
        marks['案由'][i] = marks['案由'][i].replace('罪', '')
    # 删除因为犯罪连用而产生的''
    if('' in marks['案由']):
        marks_ay_set = set(marks['案由'])
        marks_ay_set.remove('')
        marks['案由'] = list(marks_ay_set)
    if('罪行' in marks['案由']):
        marks['案由'].remove('罪行')
    if('犯罪' in marks['案由']):
        marks['案由'].remove('犯罪')
    # 至少要出现法院字
    for item in marks['相关法院']:
        if(item.find('法院') == -1):
            marks['相关法院'].remove(item)
    # 防止出现一个法院被截成部分的情况
    marks['相关法院'].sort(key=lambda i: len(i))
    remove_items = []
    for i in range(0, len(marks['相关法院'])-1):
        for j in range(i+1, len(marks['相关法院'])):
            if(marks['相关法院'][i] in marks['相关法院'][j]):
                remove_items.append(marks['相关法院'][i])
    for item in set(remove_items):
        marks['相关法院'].remove(item)
    # 防止罪行重复
    split_items = []
    for item in marks['案由']:
        if('、' in item or '一案' in item):
            split_items.append(item)

    for item in split_items:
        marks['案由'].remove(item)
        if('一案' in item):
            item = item.replace('一案', '')
        marks['案由'].extend(item.split('、'))
    # 对于词性，选取词频最高的10个
    marks['名词'] = most(freqword(marks['名词']))
    marks['动词'] = most(freqword(marks['动词']))
    marks['形容词'] = most(freqword(marks['形容词']))
    marks['副词'] = most(freqword(marks['副词']))
    # 清除重复选项
    for key, values in marks.items():
        marks[key] = list(set(values))


def save_text(case_name):  # 前端需要给出文件名
    # 保存案件文本到.txt中
    case_name = 'output\\'+case_name
    if(case_name.endswith('.txt')):
        case_name.replace('.txt', '')
    elif(case_name.endswith('.json')):
        case_name.replace('.json', '')

    with open(case_name+'.txt', 'w') as f:
        f.write(case_text)

    # 保存案件标注到.json中
    marks_copy = marks.copy()
    del marks_copy['名词']
    del marks_copy['动词']
    del marks_copy['形容词']
    del marks_copy['副词']
    with open(case_name + '.json', 'w') as f:
        json.dump(marks_copy, f, ensure_ascii=False)  # 如果True，则会保存成Unicode


def freqword(wordlis):  # 统计词频，并返回排序后的字典
    freword = {}
    for i in wordlis:
        if i in freword.keys():
            count = freword[i]
            freword[i] = count+1
        else:
            freword[i] = 1
    orderdic = sorted(freword.items(), key=operator.itemgetter(
        1), reverse=True)  # 给字典排序
    return orderdic


def most(l):
    l = l[0:10]
    most_words = []
    for item in l:
        most_words.append(item[0])
    return most_words


def get_key(dic, value):
    k = [k for k, v in dic.items() if v == value]
    return k


def casemark(text):
    # 防止多次调用全局变量共享
    global tokDate
    global marks
    tokDate = {}
    marks = {}
    marks['当事人'] = []
    marks['性别'] = []
    marks['民族'] = []
    marks['出生地'] = []
    marks['案由'] = []
    # marks['相关地点'] = []
    # marks['相关时间'] = []
    # marks['出生时间'] = []
    marks['相关法院'] = []
    # 词性
    marks['名词'] = []
    marks['动词'] = []
    marks['形容词'] = []
    marks['副词'] = []
    global case_text
    case_text = text
    tok(case_text)
    mark()
    del marks['名词']
    del marks['动词']
    del marks['形容词']
    del marks['副词']
    return marks


test_label_nums = {}
test_label_nums['当事人'] = 0
test_label_nums['性别'] = 0
test_label_nums['民族'] = 0
test_label_nums['出生地'] = 0
test_label_nums['案由'] = 0
test_label_nums['相关法院'] = 0
predict_label_nums = {}
predict_label_nums['当事人'] = 0
predict_label_nums['性别'] = 0
predict_label_nums['民族'] = 0
predict_label_nums['出生地'] = 0
predict_label_nums['案由'] = 0
predict_label_nums['相关法院'] = 0
source_dir = 'all_case_and_label'
file_list = os.listdir(source_dir)
# print(file_list)
for i in range(0, len(file_list), 2):
    print(file_list[i], file_list[i+1])
    with open(os.path.join(source_dir, file_list[i]), 'r') as f:  # json
        test_label = json.load(f)

    with open(os.path.join(source_dir, file_list[i+1]), 'r') as f:  # txt
        test_txt = f.read()

    print(file_list[i+1] + ' is processing...')
    predict_label = casemark(test_txt)
    print(file_list[i+1] + ' finish')
    for word in ['当事人', '性别', '民族', '出生地', '案由', '相关法院']:
        test = test_label[word]
        predict = predict_label[word]
        test_label_nums[word] = test_label_nums[word] + 1
        if(set(test) == set(predict)):  # 防止顺序不一样而判定为不一样
            predict_label_nums[word] = predict_label_nums[word] + 1

    # print(test_label_nums)
    # print(predict_label_nums)
print('当事人 accuracy : ' +
      str(predict_label_nums['当事人']/test_label_nums['当事人']))
print('性别 accuracy : ' +
      str(predict_label_nums['性别']/test_label_nums['性别']))
print('民族 accuracy : ' +
      str(predict_label_nums['民族']/test_label_nums['民族']))
print('出生地 accuracy : ' +
      str(predict_label_nums['出生地']/test_label_nums['出生地']))
print('案由 accuracy : ' +
      str(predict_label_nums['案由']/test_label_nums['案由']))
print('相关法院 accuracy : ' +
      str(predict_label_nums['相关法院']/test_label_nums['相关法院']))
