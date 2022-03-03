# from selenium import webdriver
# options=webdriver.ChromeOptions()
# options.add_experimental_option("debuggerAddress","127.0.0.1:9527")
# driver=webdriver.Chrome(options=options)
# print(driver.title)
import time
import datetime

now_time = datetime.datetime.now()

date = now_time + datetime.timedelta(days=2)

new_time = date.strftime('%Y-%m-%d')

url = f'https://elife.fudan.edu.cn/public/front/getResource2.htm?contentId=8aecc6ce749544fd01749a31a04332c2&ordersId=&currentDate={new_time}'
print(f'{new_time} done!')
print(url)