'''
由训练集和测试集，根据人工设计构建的词向量，输入多项式朴素贝叶斯模型中进行训练并用测试集进行测试评估
需要训练集，测试集的文本、将它们中的所需要分类的词语放到data文件夹下的各个文本txt中，用于给输入的词打标签

调用说明：如果是用于分词和提取文本只需要调用predict_for_txt(content, model_path)即可，返回字典
'''
# import logging
# import gensim
# from gensim.models import word2vec
import jieba
import jieba.posseg
import os
from sklearn.naive_bayes import MultinomialNB
# import matplotlib.pyplot as plt
# from sklearn.metrics import classification_report
from sklearn.decomposition import PCA
from matplotlib import pyplot
import joblib  # 用于保存模型

path = os.path.join(os.getcwd(), 'mark')

def load_stopwords():
    '''
    加载停词表
    :return:stopwords:停词表列表
    '''
    stopwords = []
    with open(os.path.join(path, 'my_stopwords.txt'), "r", encoding='utf-8-sig') as f:
        lines = f.readlines()
        for line in lines:
            stopwords.append(line.strip())
    return stopwords


def load_rece_list():
    '''
    加载所有的民族
    :return:stopwords:民族列表
    '''
    race_list = []
    with open(os.path.join(path, 'word2vec/data/race.txt'), 'r', encoding='utf-8') as f:
        race_list = f.read().split('、')
    return race_list


def combine_words_for_courts_locations(words_after_filter):
    '''
    将被分词分开的法院和地名进行，返回合并后的法院和地名的列表用于后续处理
    :parameter:words_after_filter:经过停词表过滤的词列表
    :return:courts, locations:合并后的法院和地名的列表
    '''
    courts = []
    locations = []
    for i in range(0, len(words_after_filter)):
        word = words_after_filter[i]
        if word.flag == 'nt' and '院' in word.word:  # 合并所有的法院名
            new_word = word.word
            j = i
            while(j >= 0):
                j = j-1
                if words_after_filter[j].flag in ['ns', 'm', 'b']:
                    new_word = words_after_filter[j].word + new_word
                else:
                    break
            courts.append(new_word)

        elif word.flag == 'ns':  # 合并所有的地名
            new_word = word.word
            times = 0  # 至少要两次
            while(i < len(words_after_filter)):
                i = i+1
                if words_after_filter[i].flag in ['ns', 'x', 'zg', 'm'] or (words_after_filter[i].flag == 'n' and words_after_filter[i].word in ['沟', '乡', '村', '镇', '号']):
                    new_word = new_word + words_after_filter[i].word
                    times = times + 1
                else:
                    break
            if times >= 1:
                # print(new_word)
                locations.append(new_word)

    return courts, locations


def preprocess(content, stopwords):
    '''
    对文本进行预处理，即调用combine_words_for_courts_locations将法院和地名进行合并，将得到的合并的结果加入分词词典中，防止被分开，返回处理后的分词list
    :parameter:content:文本
    :parameter:stopwords:停词列表
    :return:words_after_filter:处理后的分词list
    '''
    words = jieba.posseg.lcut(content.strip())
    # print(stopwords)
    words_after_filter = []
    for word in words:
        if word.word not in stopwords and word.word != ' ' and word.word != '\n':
            words_after_filter.append(word)
    # print(words_after_filter)
    courts, locations = combine_words_for_courts_locations(words_after_filter)
    for court in set(courts):
        jieba.add_word(court, tag='nt')
    for location in locations:
        jieba.add_word(location, tag='ns')
    # 经过预处理增加用户词典(处理被拆开的法院名和地名)，从而精准分词
    words = jieba.posseg.lcut(content.strip())
    words_after_filter = []
    for word in words:
        if word.word not in stopwords and word.word != ' ' and word.word != '\n':
            words_after_filter.append(word)
    # print(words_after_filter)
    return words_after_filter


def TextFeatures(words_after_filter, race_list, features_list):
    '''
    构建词向量
    :parameter:words_after_filter:处理后的分词list
    :parameter:race_list:民族列表
    :parameter:features_list:特征向量列表，从而可以持续地调用这个函数来将所有的词向量加入特征向量列表中
    :return:features_list:补充后的词向量
    '''
    for i in range(0, len(words_after_filter)):
        word = words_after_filter[i]
        featureVector = []
        # for j in range(0, 10):
        featureVector.append(
            1 if(words_after_filter[i-1].word in ['被告人', '罪犯']) else 0)
        featureVector.append(
            1 if(word.word == '男' or word.word == '女') else 0)
        featureVector.append(
            1 if(words_after_filter[i-1].word == '犯') else 0)
        featureVector.append(1 if('罪' in word.word) else 0)
        featureVector.append(
            1 if(words_after_filter[i-1].word == '生于' or words_after_filter[i-1].word == '出生') else 0)
        featureVector.append(
            1 if('省' in word.word) else 0)
        featureVector.append(
            1 if('市' in word.word) else 0)
        featureVector.append(
            1 if(word.word in race_list) else 0)
        featureVector.append(
            1 if('法院' in word.word) else 0)
        featureVector.append(1 if(word.flag == 'nr') else 0)
        featureVector.append(1 if(word.flag == 'nz') else 0)
        featureVector.append(1 if(word.flag == 'ns') else 0)
        featureVector.append(1 if(word.flag == 'nt') else 0)
        featureVector.append(1 if(word.flag == 'i') else 0)
        featureVector.append(1 if(word.flag == 'l') else 0)
        featureVector.append(1 if(word.flag == 'b') else 0)
        featureVector.append(1 if(word.flag == 'm') else 0)
        featureVector.append(1 if(word.flag == 'n') else 0)
        featureVector.append(1 if(word.flag == 'v') else 0)
        # print(featureVector)
        features_list.append(featureVector)
    return features_list


def load_labels():
    '''
    加载人工的标注
    :return:labels:将data下的人工标注加载进来得到的字典
    '''
    labels = {}
    labels['person'] = []
    labels['sex'] = []
    labels['race'] = []
    labels['crime'] = []
    labels['location'] = []
    labels['court'] = []

    with open(os.path.join(path, 'word2vec/data/person.txt'), 'r', encoding='utf-8') as f:
        txt = f.read()
        txt_list = txt.split(' ')
        labels['person'] = txt_list
    with open(os.path.join(path, 'word2vec/data/sex.txt'), 'r', encoding='utf-8') as f:
        txt = f.read()
        txt_list = txt.split(' ')
        labels['sex'] = txt_list
    with open(os.path.join(path, 'word2vec/data/race.txt'), 'r', encoding='utf-8') as f:
        txt = f.read()
        txt_list = txt.split('、')
        labels['race'] = txt_list
    with open(os.path.join(path, 'word2vec/data/crime.txt'), 'r', encoding='utf-8') as f:
        txt = f.read()
        txt_list = txt.split(' ')
        labels['crime'] = txt_list
    with open(os.path.join(path, 'word2vec/data/location.txt'), 'r', encoding='utf-8') as f:
        txt = f.read()
        txt_list = txt.split(' ')
        labels['location'] = txt_list
    with open(os.path.join(path, 'word2vec/data/court.txt'), 'r', encoding='utf-8') as f:
        txt = f.read()
        txt_list = txt.split(' ')
        labels['court'] = txt_list
    return labels


def label_for_word(labels, words_after_filter, label_list):
    '''
    根据加载好的人工标注给每一个词进行分类，生成对应的label_list
    :parameter:labels:人工标注字典
    :parameter:words_after_filter:处理后的词列表
    :parameter:label_list:标签列表，从而可以持续地调用这个函数来将所有的标签对应地加入标签列表中
    :return:features_list:补充后的标签列表
    '''
    for word in words_after_filter:
        if word.word in labels['person']:
            label_list.append('person')
        elif word.word in labels['court']:
            label_list.append('court')
        elif word.word in labels['location']:
            label_list.append('location')
        elif word.word in labels['race']:
            label_list.append('race')
        elif word.word in labels['sex']:
            label_list.append('sex')
        elif word.word in labels['crime']:
            label_list.append('crime')
        else:
            label_list.append('other')
    return label_list


def generate_wordvector_and_labellist(source_dir, stopwords):
    '''
    对文件夹中的每一个文本进行分词，同时预处理得到最终分词，再把每一个词转换成词向量添加到feature_list中
    将每个词所属的类别加到label_list中，返回词向量列表和对应的类别列表（一一对应关系）
    :param source_dir:文件夹
    :param stopwords:停词列表
    :return: feature_list, label_list
    '''
    feature_list = []
    label_list = []
    file_list = os.listdir(source_dir)
    for file in file_list:
        source = os.path.join(source_dir, file)
        with open(source, 'r', encoding='gbk') as f:
            content = f.read()
        words_after_filter = preprocess(content, stopwords)
        feature_list = TextFeatures(
            words_after_filter, load_rece_list(), feature_list)
        label_list = label_for_word(
            load_labels(), words_after_filter, label_list)
    return feature_list, label_list


def train_and_save_model(train_feature_list, train_label_list, dir):
    '''
    训练并且保存模型
    :param train_feature_list:用于训练的特征向量列表
    :param train_label_list:特征向量一一对应的标签
    :param dir:保存的模型所在目录
    :return: feature_list, label_list
    '''
    classifier = MultinomialNB().fit(train_feature_list, train_label_list)
    joblib.dump(classifier, dir + '\\' + "MultinomialNB_model.m")
    print('model has been saved in ' + dir + '\\' + "MultinomialNB_model.m")


def get_train_and_test_set(train_dir, test_dir):
    '''
    :param train_dir:训练文本所在目录
    :param test_dir:测试文本所在目录
    :return: train_feature_list, train_label_list, test_feature_list, test_label_list:训练集测试集词向量列表，词向量列表对应的类别
    '''
    train_feature_list, train_label_list = generate_wordvector_and_labellist(
        'train_case', load_stopwords())
    test_feature_list, test_label_list = generate_wordvector_and_labellist(
        'test_case', load_stopwords())
    return train_feature_list, train_label_list, test_feature_list, test_label_list


def pca_and_plt_show(feature_list, label_list):
    '''
    对特征向量进行PCA降维后展示分类结果
    :param feature_list:特征向量列表
    :param label_list:特征向量对应的标签列表
    '''
    X = feature_list
    pca = PCA(n_components=2)
    result = pca.fit_transform(X)
    # 可视化展示
    pyplot.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    pyplot.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    pyplot.scatter(result[:, 0], result[:, 1])
    words = label_list
    for i, word in enumerate(words):
        pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
    pyplot.show()


def predict_for_txt(content, model_path):  # 给一个文本分词并预测其中的每一个词，得到字典
    '''
    给一个文本分词并预测其中的每一个词，得到字典
    :param content:str文本
    :param model_path:朴素贝叶斯模型的路径
    :return:marks:字典包含下面的多个类型的列表，用于展示结果
    '''
    print('loading model...')
    classifier = joblib.load(model_path)  # 加载模型
    print('load model successfully')
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

    words_after_filter = preprocess(content, load_stopwords())
    features_list = []
    features_list = TextFeatures(
        words_after_filter, load_rece_list(), features_list)

    predict = classifier.predict(features_list)
    for word, label in zip(words_after_filter, predict):
        if(label == 'person'):
            marks['当事人'].append(word.word)
        elif(label == 'sex'):
            marks['性别'].append(word.word)
        elif(label == 'race'):
            marks['民族'].append(word.word)
        elif(label == 'location'):
            marks['出生地'].append(word.word)
        elif(label == 'crime'):
            marks['案由'].append(word.word)
        elif(label == 'court'):
            marks['相关法院'].append(word.word)
    marks['性别'] = [marks['性别'][0]]
    marks['当事人'] = [marks['当事人'][0]]

    for word in words_after_filter:
        if(word.flag == 'v'):
            marks['动词'].append(word.word)
        elif(word.flag == 'a'):
            marks['形容词'].append(word.word)
        elif(word.flag == 'd'):
            marks['副词'].append(word.word)

    for key, values in marks.items():
        if(key != '名词'):  # 名词列表不处理，防止打乱顺序
            marks[key] = list(set(values))

    for key in ['当事人', '性别', '民族', '出生地', '案由', '相关法院']:
        marks['名词'].extend(marks[key])
    marks['动词'] = marks['动词'][0:7]
    marks['形容词'] = marks['形容词'][0:7]
    marks['副词'] = marks['副词'][0:7]

    return marks


def get_keyword(content):
    """
    提取文本中的关键词
    :param content:被提取文本
    :return:keyword1, keyword2:tf-idf方式提取的关键词，textrank方式提取的关键词
    """
    tfidf = jieba.analyse.extract_tags
    textrank = jieba.analyse.textrank
    # 基于TF-IDF算法进行关键词抽取
    keyword1 = tfidf(content, topK=20, withWeight=True)
    # 基于textrank算法进行关键词抽取
    keyword2 = textrank(content, topK=20, withWeight=True)
    return keyword1, keyword2
