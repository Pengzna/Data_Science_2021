from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


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
        for word in dic['户籍地']:
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
    # urls = {
    #     'criminal': criminal_url,
    #     'case': case_url,
    #     'hall': hall_url
    # }
    # return urls


def handle_date2image(text, type):
    fontpath = './assets/方正苏新诗柳楷简体.ttf'
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
    word_cloud.to_file("D:/vueproject/src/assets/" + type + ".jpg")
    # plt.figure(dpi=100)  # 通过这里可以放大或缩小
    # plt.imshow(wc, interpolation='catrom', vmax=1000)
    # plt.axis("off")  # 隐藏坐标


if __name__ == '__main__':
    test = {'名词': ['云南省', '云南省高级人民法院', '中华人民共和国最高人民法院', '呼伦贝尔市×××市×××镇××街×××号', '汉族', '辽宁省', '吕某某', '营口市人民检察院',
              '辽宁省营口市中级人民法院', '云南省临沧市中级人民法院', '文山', '男', '辽宁省高级人民法院', '故意杀人罪', '中华人民共和国', '张学良'],
             '动词': ['执行', '剥夺', '服刑', '作出', '审理', '缓期', '判处', '进行', '核准', '减刑'],
             '形容词': ['严重', '大', '最高', '确实', '亲密', '恶劣', '高级', '残忍', '清楚', '充分'],
             '副词': ['没有', '亦', '遂', '已', '依法', '当场', '同年', '故意', '先后', '确'],
             '当事人': ['张学良'],
             '性别': ['男'],
             '民族': ['汉族'],
             '户籍地': ['呼伦贝尔市×××市×××镇××街×××号'],
             '案由': ['故意杀人罪'],
             '相关地点': ['云南省', '辽宁省', '呼伦贝尔市', '耿马县', '营口市', '内蒙古自治区', '中华人民共和国'],
             '相关时间': ['2020年2月19日', '二〇二一年七月十七日', '2017年7月13日', '二〇二一年三月二十四日', '1976年5月15日', '2014年8月21日', '2021年3月16日',
                      '2021年3月24日', '1974年4月20日', '2015年2月5日', '2021年3月15日', '2020年9月1日', '2020年12月11日', '2014年11月26日'],
             '出生时间': ['1974年4月20日', '1976年5月15日'],
             '相关法院': ['云南省高级人民法院', '中华人民共和国最高人民法院', '营口市人民检察院', '辽宁省营口市中级人民法院', '云南省临沧市中级人民法院', '辽宁省高级人民法院']}
    # test_res = dic2text(test, 'case')
    # print(test_res)
    # handle_date2image(test_res, 'criminal')
    envisible(test)