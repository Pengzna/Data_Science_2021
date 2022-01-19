'''
case_mark主程序，对传入的文本进行分词并提取相关需要的信息保存为字典格式后返回
如果不需要相关地点，时间，出生时间这3个选项，只要在mark函数中将相应的逻辑判断注释即可

调用说明：于分词和提取文本只需要调用casemark(text)即可，返回字典
'''
import os

import hanlp
import sys
import json
import operator
path = os.path.join(os.getcwd(), 'mark\\my_stopwords.txt')
# print(os.path.join(os.getcwd(), 'flask_backend\\mark\\my_stopwords.txt'))
HanLP = hanlp.load(
    hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH, task=["tok/fine"])  # 世界最大中文语料库
tasks = list(HanLP.tasks.keys())
for task in tasks:  # 缩减任务
    if task not in ('tok/fine', 'pos/pku', 'srl', 'ner/pku', 'ner/ontonotes'):
        del HanLP[task]
case_text = ''
stw = []
# 加载停词表
with open(path, 'r', encoding='utf-8') as f:
    stw = f.read().split('\n')

# 全局变量
tokDate = {}
marks = {}
marks['当事人'] = []
marks['性别'] = []
marks['民族'] = []
marks['出生地'] = []
marks['案由'] = []
marks['相关地点'] = []
marks['相关时间'] = []
marks['出生时间'] = []
marks['相关法院'] = []
# 词性
marks['名词'] = []
marks['动词'] = []
marks['形容词'] = []
marks['副词'] = []


def tok(content):
    '''
    使用hanlp对文本进行分词，词性标注，命名实体识别等，将tokData修改
    :param content: str文本
    '''
    global tokDate
    tokDate = json.loads(str(HanLP(content)))  # dict


def mark():
    '''
    提取文本信息，分为marks字典中的类别，填入到全局变量mark中
    '''
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
        # if(item[1] == 'nr'):
        #     marks['当事人'].append(item[0])
        if(item[1] == 'nt' and '法院' in item[0]):
            marks['相关法院'].append(item[0])
        elif(item[1] == 'ns'):
            marks['相关地点'].append(item[0])
    for item in tokDate['ner/ontonotes']:
        if(item[1] == 'DATE' and len(item[0]) >= 9):  # >=9筛选掉错误的date
            marks['相关时间'].append(item[0])
    for item in tokDate['srl']:
        if(item[1][0] == '出生'):
            marks['出生时间'].append(item[0][0])
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
    print(marks['案由'])
    for item in marks['案由']:
        print(item)
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


def save_text(case_name):
    '''
    保存案件文本和标注
    :param case_name: 要保存的文件名
    '''
    # 保存案件文本到.txt中
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


def casemark_and_save(text, path_name):
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
    save_text(path_name)
    return marks


def casemark(text):
    '''
    保存案件文本和标注
    :param text: 案件文本
    :return: 标注好的mark字典
    '''
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
    marks['相关地点'] = []
    marks['相关时间'] = []
    marks['出生时间'] = []
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
    return marks


if __name__ == '__main__':
    print(os.getcwd())  # 获取当前工作目录路径