'''
该程序用于将标注好的信息汇总到一起（即将全部的json文件读取后将其中的对应类别的词存入data下），存入data文件夹下的各个txt文件中
'''
import json
import os
source_dir = 'all_label'  # 存放json文件的文件夹
file_list = os.listdir(source_dir)
labels = {}
labels['person'] = []
labels['crime'] = []
labels['location'] = []
labels['court'] = []
# n = 0
for file in file_list:
    source = os.path.join(source_dir, file)
    with open(source, 'r', encoding='gbk') as f:
        label_dict = json.load(f)
        labels['person'].extend(label_dict['当事人'])
        labels['crime'].extend(label_dict['案由'])
        labels['location'].extend(label_dict['出生地'])
        labels['court'].extend(label_dict['相关法院'])
        # print(source + ' is ok!')
        # n = n+1
    # print(n)

with open('data\\person.txt', 'w', encoding='utf-8') as f:
    f.write(' '.join(set(labels['person'])))
with open('data\\crime.txt', 'w', encoding='utf-8') as f:
    f.write(' '.join(set(labels['crime'])))
with open('data\\location.txt', 'w', encoding='utf-8') as f:
    f.write(' '.join(set(labels['location'])))
with open('data\\court.txt', 'w', encoding='utf-8') as f:
    f.write(' '.join(set(labels['court'])))
