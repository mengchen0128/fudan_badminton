import datetime
import sys
import easyocr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
class BadmintonCrawler:

    driver_path = Service(r"chromedriver.exe")
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
        self.url = f'https://elife.fudan.edu.cn/public/front/toResourceFrame.htm?contentId=8aecc6ce749544fd01749a31a04332c2&ordersId=&currentDate={new_time}'
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

    def __getCookies(self,cookies):

        coo = {}
        coo['JSESSIONID'] = cookies[1]['value']
        coo['iPlanetDirectoryPro'] = cookies[2]['value']
        self.cookies = coo

    def __getDoc(self):

        try:


            BadmintonCrawler.driver.get(self.url)


            row =BadmintonCrawler.driver.find_elements(By.XPATH, "// table / tbody")


            before_XPath = "// table / tbody["
            aftertd_XPath = "]/ tr / td[1] / font"
            aftert_XPath = "]/ tr / td[6] / img"

            for i in range(1,len(row)):

                FinalXPath = before_XPath + str(i) + aftertd_XPath

                innerText = BadmintonCrawler.driver.find_element(By.XPATH, FinalXPath).text

                if(innerText=="12:00"):

                    FinalXPath1 = before_XPath + str(i) + aftert_XPath

                    if BadmintonCrawler.driver.find_element(By.XPATH, FinalXPath1) is not None:
                        BadmintonCrawler.driver.find_element(By.XPATH, FinalXPath1).click()
                        ele_piccaptcha = BadmintonCrawler.driver.find_element(By.CSS_SELECTOR, 'img[src="/image.jsp"]')
                        ele_piccaptcha.screenshot('./temp_capchar.png')

                        reader = easyocr.Reader(['en'], gpu=False,model_storage_directory='./model')
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

        except Exception as e:
            print(e)


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