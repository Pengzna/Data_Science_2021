# 必做：下载selenium包
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class web_Crawler(object):

    def excute(self,start,end):

        # 声明：
        # 在此过程中,为了使不被更快的识别出来以及考虑到文书网的卡顿问题，有的关键地方都设置了必要的等待，如果没有加载出来，可人为延长等待时间
        # 没有用完全加载来判定是因为这个包在我的本机会报错，为防止出问题，所以我采用了稳妥的方案

        url = 'https://wenshu.court.gov.cn/'

        # 配置基本参数,以下三种可结合,做相应的调整即可
        # 请注意,配置下面所有的参数时要保证只有一个driver=webdirver.Chrome(),并且所有的改动请通过options添加在driver=webdirver.Chrome()里面,且只有一个options

        # 可选：设定保存的目录,请注意目录分隔符windows用\\,mac用/
        # 设定下载文件的保存目录为C盘的iDownload目录，
        # 如果该目录不存在，将会自动创建
        # prefs = {"download.default_directory":"C:\\Users\\liuxi\\selenium"}
        # chromeOptions = webdriver.ChromeOptions()
        # 将自定义设置添加到Chrome配置对象实例中
        # chromeOptions.add_experimental_option("prefs", prefs)
        # driver = webdriver.Chrome(executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe",
        #                           options=chromeOptions)

        # 可选：谷歌浏览器设置为无头模式，即显不显示控制的谷歌的界面
        # opts = webdriver.ChromeOptions()
        # opts.set_headless()
        # driver = webdriver.Chrome(chrome_options=opts)
        # driver = webdriver.Chrome(executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe",options=opts)

        # 必做：下载一个Chromedriver,并且和chrome放在同一个文件夹下,将我所示的路径改为你们的Chromedriver的路径
        driver = webdriver.Chrome(executable_path="D:/Chromedriver/chromedriver.exe")

        # 选做：换IP
        # opt = webdriver.ChromeOptions()
        # opt.add_argument('--proxy-sever=http://  172.27.159.2')
        # driver = webdriver.Chrome(options=opt,executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe")

        driver.implicitly_wait(10)
        driver.get(url)
        time.sleep(2)
        driver.maximize_window()

        time.sleep(5)
        driver.find_element(By.XPATH, '//*[@id="loginLi"]/a').click()
        time.sleep(5)
        driver.refresh()

        time.sleep(30)

        el_frame = driver.find_element_by_id('contentIframe')
        driver.switch_to.frame(el_frame)

        driver.find_element_by_xpath('//*[@id="root"]/div/form/div/div[1]/div/div/div/input').send_keys('用户名')

        driver.find_element_by_xpath('//*[@id="root"]/div/form/div/div[2]/div/div/div/input').send_keys('密码')

        driver.find_element_by_xpath('//*[@id="root"]/div/form/div/div[3]/span').click()

        time.sleep(15)

        driver.find_element_by_xpath('//*[@id="_view_1540966814000"]/div/div[1]/div[1]').click()

        driver.find_element_by_xpath('//*[@id="s8"]').click()
        driver.find_element_by_xpath('//*[@id="gjjs_ajlx"]/li[3]').click()

        driver.find_element_by_xpath('//*[@id="s6"]').click()
        driver.find_element_by_xpath('//*[@id="gjjs_wslx"]/li[4]').click()

        driver.find_element(By.XPATH, '//*[@id="cprqStart"]').send_keys(start)
        driver.find_element_by_xpath('//*[@id="flyj"]').click()

        driver.find_element(By.XPATH, '//*[@id="cprqEnd"]').send_keys(end)
        driver.find_element_by_xpath('//*[@id="flyj"]').click()

        driver.find_element(By.XPATH, '//*[@id="searchBtn"]').click()

        # 或者可以用显示等待，不过可能会报其他的错
        time.sleep(60)

        # 通过改变i的范围，改变要爬取的量
        for i in range(1):
            # 等待加载出来
            while not driver.find_element_by_xpath(
                    '//*[@id="_view_1545184311000"]/div[8]/a[contains(text(),"{0}")]'.format(i + 2)).get_attribute(
                    'class') == 'active':
                driver.find_element_by_xpath('//*[@id="_view_1545184311000"]/div[8]/a[contains(text(),"下一页")]').click()
                time.sleep(5)
            el_list = driver.find_elements_by_xpath('//*[@id="_view_1545184311000"]/div/div[6]/div/a[2]')
            for j in range(len(el_list)):
                el_list[j].click()
                # 为防止被识别更慢些,操作间隙增大
                time.sleep(3)
            driver.find_element_by_link_text('下一页').click()
            time.sleep(20)
        # 增加了一行可以使浏览器爬去一定的量后自动关闭，为防止被封我现在设置的是30x5即150份
        driver.quit()
# 该函数的调用示例
# if __name__ == '__main__':
#     web_Crawler = web_Crawler()
#     更改start,end即可
#     web_Crawler.excute(start,end)

# 即,如果要调用的话,直接from Web_Crawler_3 import web_Crawler
# 然后在你需要调用的地方直接
#     web_Crawler = web_Crawler()
#     更改start,end即可
#     web_Crawler.excute(start,end)



