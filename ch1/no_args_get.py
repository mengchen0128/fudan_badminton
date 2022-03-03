import requests

url="https://www.baidu.com"
r=requests.get(url=url)
print(r.url)
print(r.status_code)
