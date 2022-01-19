import jieba
import jieba.analyse
import os
import re
import codecs
from string import digits


def getStopwords(path):
    """
    加载停用词
    :param path: txt形式的文件
    :return stopwords: 停用词列表
    """
    print("正在加载停用词...")
    stopwords = []
    with open(path, "r", encoding='utf-8-sig') as f:
        lines = f.readlines()
        for line in lines:
            stopwords.append(line.strip())
    return stopwords


def clearTXTNum(source_in_path, source_out_path):
    """
    去除文本中的数字
    :param source_in_path:
    :param source_out_path:
    """
    print("正在去除文本中的数字...")
    infile = open(source_in_path, 'r', encoding='utf-8')
    outfile = open(source_out_path, 'w', encoding='utf-8')
    for eachline in infile.readlines():
        remove_digits = str.maketrans('', '', digits)  # dict包含替换字符的映射关系
        lines = eachline.translate(remove_digits)
        # lines.encode('utf-8')
        outfile.write(lines)


def segment_line(file_list, segment_out_dir, stopwords=[]):
    '''
    字词分割，对每行进行字词分割
    :param file_list:
    :param segment_out_dir:
    :param stopwords:
    :return:
    '''
    print("正在进行分词...")
    for i, file in enumerate(file_list):
        segment_out_name = os.path.join(
            segment_out_dir, 'segment_{}.txt'.format(i))
        segment_file = open(segment_out_name, 'a', encoding='utf8')
        with open(file, encoding='utf8') as f:
            text = f.readlines()
            for sentence in text:
                # jieba.cut():参数sentence必须是str(unicode)类型
                sentence = list(jieba.cut(sentence))
                # sentence = re.sub()
                sentence_segment = []
                for word in sentence:
                    if word not in stopwords:
                        sentence_segment.append(word)
                segment_file.write(" ".join(sentence_segment))
            del text
            f.close()
        segment_file.close()


def segment_lines(source_in_dir, segment_out_dir, stopwords=[]):
    '''
    字词分割，对整个文件内容进行字词分割
    :param file_list:
    :param segment_out_dir:
    :param stopwords:
    :return:
    '''
    print("正在进行分词...")
    # jieba.load_userdict("userdict.txt")

    file_list = os.listdir(source_in_dir)
    for file in file_list:
        source = os.path.join(source_in_dir, file)
        with open(source, 'rb') as f:
            document = f.read()
            # document_decode = document.decode('GBK')
            document_cut = jieba.cut(document)
            sentence_segment = []
            for word in document_cut:
                if word not in stopwords:
                    sentence_segment.append(word)
            result = ' '.join(sentence_segment)
            result = result.encode('utf-8')
            with open(segment_out_dir, 'ab') as f2:
                f2.write(result)


if __name__ == '__main__':
    # # 文本清洗：去除数字
    # source_in_path = r'Data\\other data\\Teacher_Data.txt'
    # source_out_path = r'Data\\source\\Teachr_Data_delNum.txt'
    # clearTXTNum(source_in_path, source_out_path)

    # # 多线程分词，windows下暂时不支持
    # # jieba.enable_parallel()
    # # 加载自定义词典
    # print("正在加载自定义词典...")
    # userdict_path = r'Data\\other data\\userdict.txt'
    # jieba.load_userdict(userdict_path)

    # # 加载停用词
    # stopwords_path = r'Data\\other data\\stopwords.txt'
    # stopwords = getStopwords(stopwords_path)

    # # 实现分词
    # source_in_dir = r'Data\\source'
    # segment_out_dir = r'Data\\segmen_result\\seg_result_new.txt'
    # segment_lines(source_in_dir, segment_out_dir, stopwords)

    # # 提取分词结果中的关键词，使用TF-IDF
    # keyword_path = r'Data\\keword_result\\keyword_result_new.txt'
    # get_keyword(segment_out_dir, keyword_path)

    # 多线程分词，windows下暂时不支持
    # jieba.enable_parallel()
    # 加载自定义词典

    # 加载停用词
    stopwords_path = r'my_stopwords.txt'
    stopwords = getStopwords(stopwords_path)

    # 实现分词
    source_in_dir = r'train_case'
    segment_out_dir = r'seg_case.txt'
    segment_lines(source_in_dir, segment_out_dir, stopwords)
