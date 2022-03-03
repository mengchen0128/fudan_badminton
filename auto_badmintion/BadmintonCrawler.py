import datetime
import sys
import easyocr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By



class BadmintonCrawler:

    driver_path = Service(r"D:\python\chromedriver.exe")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=driver_path, options=options)

    now_time = datetime.datetime.now()
    date = now_time + datetime.timedelta(days=2)
    new_time = date.strftime('%Y-%m-%d')
    #driver = webdriver.Firefox()
    def __init__(self):
        now_time = datetime.datetime.now()
        date = now_time + datetime.timedelta(days=2)
        new_time = date.strftime('%Y-%m-%d')
        self.url = f'https://elife.fudan.edu.cn/public/front/getResource2.htm?contentId=2c9c486e4f821a19014f82418a900004&ordersId=&currentDate={new_time}'
        self.__login()

    def __login(self):

        url = "https://uis.fudan.edu.cn/authserver/login?service=https%3A%2F%2Felife.fudan.edu.cn%2Flogin2.action"
        BadmintonCrawler.driver.get(url)
        BadmintonCrawler.driver.find_element(By.ID,"username").send_keys("20210860053")
        BadmintonCrawler.driver.find_element(By.ID,"password").send_keys("fDu120031")
        BadmintonCrawler.driver.find_element(By.ID,"idcheckloginbtn").click()
        #显示等待

        cookies = BadmintonCrawler.driver.get_cookies()
        self.__getCookies(cookies)
        #driver.quit()

    def __getCookies(self,cookies):

        coo = {}
        coo['JSESSIONID'] = cookies[1]['value']
        coo['iPlanetDirectoryPro'] = cookies[2]['value']
        self.cookies = coo

    def __getDoc(self):

        try:

            # r = requests.get(self.url, cookies=self.cookies)
            # r.raise_for_status()  # 若请求不成功,抛出HTTPError 异常
            # doc = pq(r.text)
            # times = []
            # trList = doc(".site_table .site_tr")
            # for tr in trList.items():
            #     imgSrc = str(tr("td[align='right'] img").attr('src'))
            #     if 'reserve.gif' in imgSrc:
            #         times += [tr('.site_td1:first-child font').text()]
                #if(tr('.site_td1:first-child font').text()=='18:00'):

            BadmintonCrawler.driver.get(self.url)

            # mytable = BadmintonCrawler.driver.find_element(By.TAG_NAME,"site_table")
            #
            # list=mytable.find_element(By.TAG_NAME("tr"))
            #
            # text=list.find_element(By.TAG_NAME("td"))


            row =BadmintonCrawler.driver.find_elements(By.XPATH, "// table / tbody")

            #print(len(row))

            before_XPath = "// table / tbody["
            aftertd_XPath = "]/ tr / td[1] / font"
            aftert_XPath = "]/ tr / td[6] / img"
            aftertr_XPath = "]"

            for i in range(1,len(row)):

                FinalXPath = before_XPath + str(i) + aftertd_XPath

                innerText = BadmintonCrawler.driver.find_element(By.XPATH, FinalXPath).text

                if(innerText=="12:00"):

                    print(innerText)

                    FinalXPath1 = before_XPath + str(i) + aftert_XPath

                    if BadmintonCrawler.driver.find_element(By.XPATH, FinalXPath1) is not None:
                        BadmintonCrawler.driver.find_element(By.XPATH, FinalXPath1).click()
                        ele_piccaptcha = BadmintonCrawler.driver.find_element(By.CSS_SELECTOR, 'img[src="/image.jsp"]')
                        ele_piccaptcha.screenshot('./temp_capchar.png')

                        reader = easyocr.Reader(['en'], gpu=False)
                        cc = reader.readtext('./temp_capchar.png', detail=0)

                        while ' ' in cc:
                            cc.remove('')

                        BadmintonCrawler.driver.find_element(By.ID, "imageCodeName").send_keys(cc)
                        BadmintonCrawler.driver.find_element(By.ID, "btn_sub").click()



                        dig_confirm = BadmintonCrawler.driver.switch_to.alert

                        dig_confirm.accept()

                        if 'reserve.gif' in dig_confirm.text:
                            pass


            BadmintonCrawler.driver.close()



            # / html / body / div[2] / div[2] / div[2] / div / table / tbody[1] / tr / td[1]
            # // *[ @ id = "con_one_1"] / table / tbody[1] / tr / td[6] / img
            # / html / body / div[2] / div[2] / div[2] / div / table / tbody[1] / tr / td[6] / img

            # BadmintonCrawler.driver.find_element(By.CSS_SELECTOR,'img[src="/images/front/index/button/reserve.gif"]').click()
            #
            #
            # print('当前浏览地址为：.{0}'.format(BadmintonCrawler.driver.current_url))
            #
            # # 先找到验证码对应的网页元素
            # ele_piccaptcha = BadmintonCrawler.driver.find_element(By.CSS_SELECTOR,'img[src="/image.jsp"]')
            # # 然后直接调用这个元素的screenshot方法，参数是保存的路径即可实现截图
            # ele_piccaptcha.screenshot('./temp_capchar.png')
            #


            #return times


        except Exception as e:
            print(e)

        # url1=BadmintonCrawler.driver.current_url
        # r1 = requests.get(url1, cookies=self.cookies)
        # print(r1.status_code)

        # driver.find_element_by_xpath("//img[@src='/images/front/index/button/reserve.gif']").click()


    def run(self):
        times = self.__getDoc()

        if times:
            print(times)


if __name__ == '__main__':
    bc = BadmintonCrawler()

    bc.run()

    now_time = datetime.datetime.now()

    new_time = now_time.strftime('%Y-%m-%d')

    print(f'{new_time} done!')

    sys.exit()