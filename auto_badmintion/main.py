import json
import time
import os
from json import loads as json_loads
from os import path as os_path, getenv
from sys import exit as sys_exit
from pyquery import PyQuery as pq
from getpass import getpass
import re
import base64
import io
import numpy
import requests
from PIL import Image
from PIL import ImageEnhance

from requests import session, post, adapters
adapters.DEFAULT_RETRIES = 5

class Fudan:
    """
    建立与复旦服务器的会话，执行登录/登出操作
    """
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"

    # 初始化会话
    def __init__(self,
                 uid, psw, url,
                 url_login='https://uis.fudan.edu.cn/authserver/login?service=https%3A%2F%2Felife.fudan.edu.cn%2Flogin2.action',
                 url_code="https://zlapp.fudan.edu.cn/backend/default/code",
                 ):
        """
        初始化一个session，及登录信息
        :param uid: 学号
        :param psw: 密码
        :param url_login: 登录页，默认服务为空
        """
        self.session = session()
        self.session.keep_alive = True # 改为持久连接
        self.session.headers['User-Agent'] = self.UA
        self.url_login = url_login
        self.url_code = url_code

        self.uid = uid
        self.psw = psw
        self.cookies=[]
    def _page_init(self):
        """
        检查是否能打开登录页面
        :return: 登录页page source
        """
        print("◉Initiating——", end='')
        page_login = self.session.get(self.url_login)
        self.cookies = page_login.cookies

        #self.__getCookies(cookies)

        print("return status code",
              page_login.status_code)

        if page_login.status_code == 200:
            print("◉Initiated——", end="")
            return page_login.text
        else:
            print("◉Fail to open Login Page, Check your Internet connection\n")
            self.close()

    def login(self):
        """
        执行登录
        """
        page_login = self._page_init()

        print("getting tokens")
        data = {
            "username": self.uid,
            "password": self.psw,
            "service": "https://zlapp.fudan.edu.cn/site/ncov/fudanDaily"
        }

        # 获取登录页上的令牌
        result = re.findall(
            '<input type="hidden" name="([a-zA-Z0-9\-_]+)" value="([a-zA-Z0-9\-_]+)"/?>', page_login)
        # print(result)
        # result 是一个列表，列表中的每一项是包含 name 和 value 的 tuple，例如
        # [('lt', 'LT-6711210-Ia3WttcMvLBWNBygRNHdNzHzB49jlQ1602983174755-7xmC-cas'), ('dllt', 'userNamePasswordLogin'), ('execution', 'e1s1'), ('_eventId', 'submit'), ('rmShown', '1')]
        data.update(
            result
        )

        headers = {
            "Host": "uis.fudan.edu.cn",
            "Origin": "https://uis.fudan.edu.cn",
            "Referer": self.url_login,
            "User-Agent": self.UA
        }

        print("◉Login ing——", end="")
        post = self.session.post(
            self.url_login,
            data=data,
            headers=headers,
            allow_redirects=False)


        print("return status code", post.status_code)

        if post.status_code == 302:
            print("\n***********************"
                  "\n◉登录成功"
                  "\n***********************\n")
        else:
            print("◉登录失败，请检查账号信息")
            self.close()

    def __getCookies(self,cookies):
        coo = {}
        coo['JSESSIONID'] = cookies[1]['value']
        coo['iPlanetDirectoryPro'] = cookies[2]['value']
        self.cookies = coo

    def logout(self):
        """
        执行登出
        """
        exit_url = 'https://uis.fudan.edu.cn/authserver/logout?service=/authserver/login'
        expire = self.session.get(exit_url).headers.get('Set-Cookie')
        # print(expire)

        if '01-Jan-1970' in expire:
            print("◉登出完毕")
        else:
            print("◉登出异常")

    def close(self, exit_code=0):
        """
        执行登出并关闭会话
        """
        self.logout()
        self.session.close()
        print("◉关闭会话")
        print("************************")
        sys_exit(exit_code)


class Zlapp(Fudan):
    last_info = ''

    def run(self):
        doc = self.__getDoc()
        times = self.checkEmpty(doc)
        if times:
            print(times)



    def __getDoc(self):
        try:
            print(self.cookies)
            r = requests.get(url,cookies=self.cookies)
            r.raise_for_status()  # 若请求不成功,抛出HTTPError 异常
            doc = pq(r.text)
            return doc
        except Exception as e:
            print(e)

    def check(self):
        pass




    def checkEmpty(self, doc):
        times = []
        trList = doc(".site_table .site_tr")
        for tr in trList.items():
            imgSrc = str(tr("td[align='right'] img").attr('src'))
            if 'reserve.gif' in imgSrc:
                times += [tr('.site_td1:first-child font').text()]

        return times


def get_account():
    """
    获取账号信息
    """
    uid = getenv("STD_ID")
    psw = getenv("PASSWORD")
    if uid != None and psw != None:
        print("从环境变量中获取了用户名和密码！")
        return uid, psw
    print("\n\n请仔细阅读以下日志！！\n请仔细阅读以下日志！！！！\n请仔细阅读以下日志！！！！！！\n\n")
    if os_path.exists("account.txt"):
        print("读取账号中……")
        with open("account.txt", "r") as old:
            raw = old.readlines()
        if (raw[0][:3] != "uid") or (len(raw[0]) < 10):
            print("account.txt 内容无效, 请手动修改内容")
            sys_exit()
        uid = (raw[0].split(":"))[1].strip()
        psw = (raw[1].split(":"))[1].strip()

    else:
        pass

    return uid, psw


if __name__ == '__main__':
    uid, psw = get_account()
    # print(uid, psw)
    zlapp_login = 'https://uis.fudan.edu.cn/authserver/login?service=https%3A%2F%2Felife.fudan.edu.cn%2Flogin2.action'
    code_url = "https://zlapp.fudan.edu.cn/backend/default/code"

    url = "https://elife.fudan.edu.cn/public/front/getResource2.htm?contentId=8aecc6ce749544fd01749a31a04332c2&ordersId=&currentDate=2022-03-03"

    daily_fudan = Zlapp(uid, psw, url=url,
                        url_login=zlapp_login, url_code=code_url,)
    daily_fudan.login()
    daily_fudan.run()
    daily_fudan.close(1)



