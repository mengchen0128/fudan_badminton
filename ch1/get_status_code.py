

import requests

url = "http://www.httpbin.org/#/HTTP_Methods/get_get"
r=requests.get(url)
print(r.status_code)