from gensim.models import word2vec
import multiprocessing
from sklearn.decomposition import PCA
from matplotlib import pyplot
from sklearn.naive_bayes import GaussianNB


def train_wordVectors(sentences, embedding_size=128, window=5, min_count=5):
    '''
    :param sentences: sentences可以是LineSentence或者PathLineSentences读取的文件对象，也可以是
                    The `sentences` iterable can be simply a list of lists of tokens,如lists=[['我','是','中国','人'],['我','的','家乡','在','广东']]
    :param embedding_size: 词嵌入大小
    :param window: 窗口
    :param min_count:Ignores all words with total frequency lower than this.
    :return: w2vModel
    '''
    w2vModel = word2vec.Word2Vec(sentences, vector_size=embedding_size, window=window, min_count=min_count,
                                 workers=multiprocessing.cpu_count(), epochs=10)
    return w2vModel


def save_wordVectors(w2vModel, word2vec_path):
    w2vModel.save(word2vec_path)
    w2vModel.wv.save_word2vec_format(word2vec_path + '.txt', binary=False)


def load_wordVectors(word2vec_path):
    w2vModel = word2vec.Word2Vec.load(word2vec_path)
    return w2vModel


def plt_show(word2vec_model):
    '''
    :param word2vec_model: 需要PCA降维可视化的词向量集合，即word2vec的模型
    '''
    X = word2vec_model.wv[word2vec_model.wv.key_to_index]
    pca = PCA(n_components=2)
    result = pca.fit_transform(X)
    # 可视化展示
    pyplot.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    pyplot.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    pyplot.scatter(result[:, 0], result[:, 1])
    words = list(word2vec_model.wv.key_to_index)
    for i, word in enumerate(words):
        pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
    pyplot.show()


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

    with open('data\\person.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
        txt_list = txt.split(' ')
        labels['person'] = txt_list
    with open('data\\sex.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
        txt_list = txt.split(' ')
        labels['sex'] = txt_list
    with open('data\\race.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
        txt_list = txt.split('、')
        labels['race'] = txt_list
    with open('data\\crime.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
        txt_list = txt.split(' ')
        labels['crime'] = txt_list
    with open('data\\location.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
        txt_list = txt.split(' ')
        labels['location'] = txt_list
    with open('data\\court.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
        txt_list = txt.split(' ')
        labels['court'] = txt_list
    return labels


if __name__ == '__main__':
    segment_path = 'seg_case.txt'
    sentences = word2vec.LineSentence(segment_path)
    word2vec_path = 'model\\word_vecs'

    model2 = train_wordVectors(
        sentences, embedding_size=128, window=5, min_count=1)  # 参数需要调整才会比较准确
    save_wordVectors(model2, word2vec_path)
    word_feature_dic = {}
    feature_list = []
    class_list = []
    for word in model2.wv.index_to_key:
        word_feature_dic[word] = model2.wv[word]
        feature_list.append(word_feature_dic[word])

    # plt_show(model2)
    labels = load_labels()

    useful_feature_list = []
    useful_word_list = []
    for word in word_feature_dic.keys():
        if word in labels['person']:
            class_list.append('person')
            useful_feature_list.append(word_feature_dic[word])
            useful_word_list.append(word)
        elif word in labels['sex']:
            class_list.append('sex')
            useful_feature_list.append(word_feature_dic[word])
            useful_word_list.append(word)

        elif word in labels['race']:
            class_list.append('race')
            useful_feature_list.append(word_feature_dic[word])
            useful_word_list.append(word)

        elif word in labels['crime']:
            class_list.append('crime')
            useful_feature_list.append(word_feature_dic[word])
            useful_word_list.append(word)

        elif word in labels['location']:
            class_list.append('location')
            useful_feature_list.append(word_feature_dic[word])
            useful_word_list.append(word)

        elif word in labels['court']:
            class_list.append('court')
            useful_feature_list.append(word_feature_dic[word])
            useful_word_list.append(word)
        else:
            class_list.append('other')
    # with open('class_list.txt', 'w') as f:
    #     f.write(str(class_list))
    # with open('feature_list.txt', 'w') as f:
    #     f.write(str(feature_list))
    # print(len(word_feature_dic))
    # print(model2.wv.similarity('佟亮', '被告人'))
    # print(model2.wv.most_similar_cosmul('佟亮'))

    # test_list = useful_feature_list[100:]
    # classifier = GaussianNB().fit(useful_feature_list[:100], class_list[:100])

    # predict = classifier.predict(test_list)
    # print(predict)
    # print(class_list[100:])

    # test_accuracy = classifier.score(test_list, class_list[100:])
    # print(test_accuracy)
