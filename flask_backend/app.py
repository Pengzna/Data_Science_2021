import json
import os

from flask import Flask
from flask import request
from flask_cors import *
# import case_mark
from mark import case_mark
from mark import naive_bayes
from crawler import Web_Crawler
from wordcloud import WordCloud

app = Flask(__name__)
caseText = ''
# 解决跨域问题
CORS(app, supports_credentials=True)


@app.route('/data-science', methods=['GET', 'POST'])
def test_axios():
    return "HIT GOOD TRAP!"


@app.route('/onSpider', methods=['GET', 'POST', 'OPTIONS'])
def handleSpider():
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST'
    }
    if request.method == 'POST':
        data = request.json
        startTime = data.get('startTime').replace('/', '-')
        endTime = data.get('endTime').replace('/', '-')
        print(startTime, endTime)
        web_crawler = Web_Crawler.web_Crawler()
        web_crawler.excute(startTime, endTime)
        print('Crawler done.')
        return 'Crawler done.'
    # 调用爬虫函数，将文件保存到本地
    return "HIT GOOD TRAP!"


@app.route('/onSplit', methods=['GET', 'POST', 'OPTIONS'])
def handleSplit():
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST'
    }
    if request.method == 'POST':
        data = request.json
        text = data.get('text')
        global caseText
        caseText = text
        print(text)
        # print(naive_bayes.get_keyword(text))
        splitedText = naive_bayes.predict_for_txt(text, os.path.join(os.getcwd(), 'mark\\model\\MultinomialNB_model.m'))
        print('Navie bayes: ', end="")
        print(splitedText)
        res = {
            'noun': splitedText['名词'],
            'verb': splitedText['动词'],
            'adjectives': splitedText['形容词'],
            'adverb': splitedText['副词'],
        }
        # print(res)
        print('Split ok.')
        return res
    # 调用NLP，将分词结果返回给前端
    # return testText


@app.route('/onNLP', methods=['GET', 'POST', 'OPTIONS'])
def handleNLP():
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST'
    }
    if request.method == 'POST':
        data = request.json
        text = data.get('text')
        global caseText
        caseText = text
        # print(text)
        NLPedText = case_mark.casemark(text)
        print('Hanlp: ', end="")
        print(NLPedText)
        envisible(NLPedText)
        res = {
            'criminal': NLPedText['当事人'],
            'sex': NLPedText['性别'],
            'ethic': NLPedText['民族'],
            'birthPlace': NLPedText['出生地'],
            'reason': NLPedText['案由'],
            'spot': NLPedText['相关地点'],
            'time': NLPedText['相关时间'],
            'birthTime': NLPedText['出生时间'],
            'lawHall': NLPedText['相关法院'],
        }
        print('NLP ok.')
        return res
    # 调用NLP，将分词结果返回给前端


@app.route('/onMark', methods=['GET', 'POST', 'OPTIONS'])
def handleMark():
    if request.method == 'POST':
        data = request.json
        # key转中文
        data['当事人'] = data.pop('criminal')
        data['性别'] = data.pop('sex')
        data['民族'] = data.pop('ethic')
        data['出生地'] = data.pop('birth')
        data['案由'] = data.pop('reason')
        data['相关法院'] = data.pop('lawHall')
        print(data)
        # 反馈学习 更新模型
        # print('content: ' + caseText)
        # print('mark: ' + data)
        # print('path: ' + os.path.join(os.getcwd(), 'mark\\model\\MultinomialNB_model.m'))
        # naive_bayes.retrain(caseText, data, os.path.join(os.getcwd(), 'mark\\model\\MultinomialNB_model.m'))
        # 写入标注
        with open('json_result/标注.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))
        # 写入案件文本
        with open('./case_txt/案件文本.txt', 'w', encoding='utf-8') as f:
            f.write(caseText)
        print('Mark ok.')
    # 调用NLP，将分词结果返回给前端
    return 'Mark ok.'


def dic2text(dic, type):
    content = ''
    if type == 'criminal':
        for word in dic['当事人']:
            word += '，'
            content += word
        for word in dic['性别']:
            word += '，'
            content += word
        for word in dic['民族']:
            word += '，'
            content += word
        for word in dic['出生地']:
            word += '，'
            content += word
        for word in dic['出生时间']:
            word += '，'
            content += word
    elif type == 'case':
        for word in dic['案由']:
            word += '，'
            content += word
        for word in dic['相关地点']:
            word += '，'
            content += word
        for word in dic['相关时间']:
            word += '，'
            content += word
    else:
        for word in dic['相关法院']:
            word += '，'
            content += word
    return content


def envisible(text):
    criminal = dic2text(text, 'criminal')
    case = dic2text(text, 'case')
    hall = dic2text(text, 'hall')
    handle_date2image(criminal, 'criminal')
    handle_date2image(case, 'case')
    handle_date2image(hall, 'hall')


def handle_date2image(text, type):
    fontpath = './word_cloud/assets/方正苏新诗柳楷简体.ttf'
    if type == 'criminal':
        wc = WordCloud(font_path=fontpath,  # 设置字体
                       background_color="white",  # 背景颜色
                       max_words=1000,  # 词云显示的最大词数
                       max_font_size=500,  # 字体最大值
                       min_font_size=10,  # 字体最小值
                       random_state=42,  # 随机数
                       collocations=False,  # 避免重复单词
                       width=1600, height=1200, margin=10,  # 图像宽高，字间距，需要配合下面的plt.figure(dpi=xx)放缩才有效
                       )
    else:
        # if type == 'case':
        #     aimask = np.array(Image.open('./assets/law.jpg'))
        # else:
        #     aimask = np.array(Image.open('./assets/hall.png'))
        wc = WordCloud(font_path=fontpath,  # 设置字体
                       background_color="white",  # 背景颜色
                       max_words=1000,  # 词云显示的最大词数
                       max_font_size=500,  # 字体最大值
                       min_font_size=10,  # 字体最小值
                       random_state=42,  # 随机数
                       collocations=False,  # 避免重复单词
                       # mask=aimask,  # 造型遮盖
                       width=1600, height=1200, margin=10,  # 图像宽高，字间距，需要配合下面的plt.figure(dpi=xx)放缩才有效
                       )
    word_cloud = wc.generate(text)
    # 生成本地图片
    # word_cloud.to_file("D:/vueproject/src/assets/" + type + ".jpg")
    word_cloud.to_file(os.path.join(os.path.abspath('..'), 'vue_frontend\\src\\assets\\') + type + ".jpg")


if __name__ == '__main__':
    app.run()
