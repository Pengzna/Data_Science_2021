import docx
import os
from win32com import client as wc


# 由于python无法直接将doc转txt，所以
# 第一步：doc转docx
# 第二步：docx转txt

def save_doc_to_txt(rawpath, outpath):  # doc转docx
    '''
    :param rawpath: 传入和传出文件夹的路径
    :      outpath: txt文件的保存文件夹
    :return: None
    '''
    word = wc.Dispatch("Word.Application")
    # 不能用相对路径，老老实实用绝对路径
    # 需要处理的文件所在文件夹目录
    filenamelist = os.listdir(rawpath)
    for i in filenamelist:
        # 找出文件中以.doc结尾并且不以~$开头的文件（~$是为了排除临时文件的）
        if i.endswith('.doc') and not i.startswith('~$'):
            print(i)
            # try
            # 打开文件
            doc = word.Documents.Open(rawpath + i)
            # # 将文件名与后缀分割
            rename = os.path.splitext(i)
            # 将文件另存为.docx
            doc.SaveAs(rawpath + rename[0] + '.docx', 12)  # 12表示docx格式
            doc.Close()
            # 将.docx文件另存为txt
            wordapp = wc.Dispatch('Word.Application')
            doc2 = wordapp.Documents.Open(rawpath + rename[0] + '.docx')
            # 为了让python可以在后续操作中r方式读取txt和不产生乱码，参数为4
            doc2.SaveAs(outpath + rename[0] + '.txt', 4)
            doc2.Close()
    word.Quit()


if __name__ == '__main__':
    # 注意：目录的格式必须写成双反斜杠
    rawpath = 'D:\\python codes\\flaskProject\\flask_backend\\case_doc\\'
    outpath = 'D:\\python codes\\flaskProject\\flask_backend\\case_txt\\'
    save_doc_to_txt(rawpath, outpath)
    print('ok.')
