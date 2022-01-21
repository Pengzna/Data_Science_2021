# 必做：下载selenium包
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

# 未解决路径问题


# 声明：
# 在此过程中,为了使不被更快的识别出来以及考虑到文书网的卡顿问题，有的关键地方都设置了必要的等待，如果没有加载出来，可人为延长等待时间
# 没有用完全加载来判定是因为这个包在我的本机会报错，为防止出问题，所以我采用了稳妥的方案

url = 'https://anli.court.gov.cn/static/web/index.html#/alk'

# 配置基本参数,以下三种可结合,做相应的调整即可

# 可选：谷歌浏览器设置为无头模式，即显不显示控制的谷歌的界面
# opts = webdriver.ChromeOptions()
# opts.set_headless()
# driver = webdriver.Chrome(chrome_options=opts)
# driver = webdriver.Chrome(executable_path="C:/Program Files/Google/Chrome/Application/chromedriver.exe",options=opts)

# 可选：设定保存的目录
# 设定下载文件的保存目录为C盘的iDownload目录，
# 如果该目录不存在，将会自动创建
# windows \\ mac /
# chromeOptions=webdriver.ChromeOptions()
# prefs = {"download.default_directory":"C:\\Users\\liuxi"}
# 将自定义设置添加到Chrome配置对象实例中
# chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe")

# 必做：下载一个Chromedriver,并且和chrome放在同一个文件夹下,将我所示的路径改为你们的Chromedriver的路径
# driver = webdriver.Chrome(executable_path="C:/Program Files/Google/Chrome/Application/chromedriver.exe")


# 选做：换IP
# opt = webdriver.ChromeOptions()
# opt.add_argument('--proxy-sever=http://  172.27.159.2')
# driver = webdriver.Chrome(options=opt,executable_path="C:/Program Files/Google/Chrome/Application/chromedriver.exe")


# 参数的设置,传入第57和第59行，改成start,end即可
# start=input("请输入起始时间,示例：2020-12-1")
# end=input("请输入截至时间，示例，2021-12-1")


# 试图解决新的selenium不行的问题
# option = ChromeOptions()
# option.add_experimental_option('excludeSwitches', ['enable-automation'])
# driver = webdriver.Chrome(executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe",options=option)


driver.implicitly_wait(10)
driver.get(url)
time.sleep(3)
driver.maximize_window()

time.sleep(5)
driver.find_element(By.XPATH, '//*[@id="aljs"]/div/div[1]/div[2]/span').click()
time.sleep(5)

driver.find_element_by_xpath('//*[@id="aljs"]/div/div[2]/div/form/div[4]/div/div[1]/div/div/div/div[1]/input').click()

driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/ul/li[1]').click()

driver.find_element(By.XPATH, '//*[@id="aljs"]/div/div[2]/div/form/div[9]/div/button[1]/span').click()

# 抓取元素保存到文件中
# 通过设置j来设置要爬取的文书的量
for j in range(4):
    for i in range(1, 11):
        # ele = driver.find_element_by_xpath('//*[@id="right_wrap"]/div[3]/div/ul/li[' + str(i) + ']/a').text
        file = open("new"+str(j)+str(i)+".txt", "w")
        ele = driver.find_element_by_xpath(
            '//*[@id="alk"]/div[2]/div/div[2]/div[2]/ul/li['+str(i)+']/div[2]').text

        print(i, ele)
        # 去掉字符间可能存在的空格
        ss = ''.join(ele.split())
        # 写入文件
        file.write(str(i) + "  " + ss + "\n")
        # 关闭文件
        file.close()

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    driver.find_element_by_xpath('//*[@id="alk"]/div[2]/div/div[2]/div[3]/div/button[2]/i').click()
    time.sleep(5)
    driver.execute_script("window.scrollTo(0,0);")



