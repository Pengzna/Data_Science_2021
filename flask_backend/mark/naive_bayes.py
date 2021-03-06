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


if __name__ == '__main__':
    text = "中华人民共和国最高人民法院" \
           "刑 事 裁 定 书" \
           "被告人陈峰，男，汉族，1976年5月15日出生于内蒙古自治区呼伦贝尔市，初中文化，无业，户籍地呼伦贝尔市×××市×××镇××街×××号，住所地辽宁省营口市×××区××××小区××号×单元×××室。2020年2月19日被逮捕。现在押。" \
           "辽宁省营口市中级人民法院审理营口市人民检察院指控被告人陈峰犯故意杀人罪一案，于2020年9月1日以（2020）辽08刑初19号刑事附带民事判决，认定被告人陈峰犯故意杀人罪，判处死刑，剥夺政治权利终身。宣判后，在法定期限内没有上诉、抗诉。辽宁省高级人民法院经依法复核审理，于2020年12月11日以（2020）辽刑核34975455号刑事裁定，同意原审判决，并依法报请本院核准。本院依法组成合议庭，对本案进行了复核，依法讯问了被告人。现已复核终结。" \
           "经复核确认：被告人陈峰因与吕某（被害人，女，殁年31岁）之间的情感纠纷，多次到辽宁省营口市×××区×××区××号楼的对面楼座15楼楼道内，对吕某居住的××号楼×单元××××室进行观察。2020年2月1日19时许，陈峰从自己家中携带一把水果刀，又来到吕某住所对面楼座的15楼楼道内观察，因看到吕某在自己住窒内与王某（被害人，男，殁年29岁）有亲密行为，遂心生怨恨蓄意行凶报复。陈峰敲门进入吕某住室后，持水果刀先后捅刺王某的胸腹部、背部等处十余刀，捅刺吕某的颈部、胸部等处数刀，致王某、吕某当场死亡，尔后逃离现场。经鉴定：吕某符合他人持单面刃刺器刺切颈、胸部致右颈总动脉离断和上腔静脉破裂，右心室前、后壁贯通创口，造成急性大失血和严重的心脏损伤而死亡；王某符合他人持单面刃刺器刺切胸腹部致急性大失血和开放性血气胸而死亡。同年2月5日，陈峰被公安机关抓获归案。" \
           "上述事，有原审开庭审理中经质证确认的在案发现场提取的蓝色口罩，调取的汇款凭证、被告人陈峰手写的绝笔信等书证，证人吕某某、刘某某、陈某甲、黄某某、陈某乙、陈某等的证言，尸体鉴定意见、证明在提取的口罩上检见陈峰基因分型的DNA鉴定意见，现场勘验、检查笔录和辨认笔录等证据证实。被告人陈峰亦供认，足以认定。" \
           "本院认为，被告人陈峰故意非法剥夺他人生命，其行为已构成故意杀人罪。陈峰预谋杀人泄愤，当场杀死二人，犯罪手段残忍，情节特别恶劣，后果和罪行极其严重，应依法惩处。原审判决、高级人民法院复核审裁定认定的事实清楚，证据确实、充分，定罪准确，量刑适当。审判程序合法。依照《中华人民共和国刑事诉讼法》第二百四十六条、第二百五十条和《最高人民法院关于适用〈中华人民共和国刑事诉讼法〉的解释》第四百二十九条第（一）项的规定，裁定如下：" \
           "核准辽宁省高级人民法院（2020）辽刑核34975455号同意原审以故意杀人罪判处被告人陈峰死刑，剥夺政治权利终身的刑事裁定。" \
           "本裁定自宣告之日起发生法律效力。" \
           "审判长　赵　剑" \
           "审判员　魏海欢" \
           "审判员　苏　敏" \
           "二〇二一年七月十七日" \
           "书记员　张名嘉"
    print(get_keyword(text))


def retrain(content, marks, model_path):
    classifier = joblib.load(model_path)  # 加载模型
    words_after_filter = preprocess(content, load_stopwords())
    features_list = []
    features_list = TextFeatures(
        words_after_filter, load_rece_list(), features_list)
    train_feature_list = []
    train_label_list = []
    for feature, word in zip(features_list, words_after_filter):
        if(word.word in marks['当事人']):
            train_feature_list.append(feature)
            train_label_list.append('person')
        elif(word.word in marks['性别']):
            train_feature_list.append(feature)
            train_label_list.append('sex')
        elif(word.word in marks['民族']):
            train_feature_list.append(feature)
            train_label_list.append('race')
        elif(word.word in marks['出生地']):
            train_feature_list.append(feature)
            train_label_list.append('location')
        elif(word.word in marks['案由']):
            train_feature_list.append(feature)
            train_label_list.append('crime')
        elif(word.word in marks['相关法院']):
            train_feature_list.append(feature)
            train_label_list.append('court')
    print(train_feature_list)
    print(train_label_list)
    classifier.partial_fit(train_feature_list, train_label_list)
    joblib.dump(classifier, model_path)