if 5 == 10 - 6 + 1:
    print('panduan')

import re

pattern = r'https://security\.snyk\.io/vuln/.*$'
pattern2 = r'https://security\.snyk\.io/vuln/(\d+)'
url = 'https://security.snyk.io/vuln/30'
url2 = 'https://security.snyk.io/vuln/SNYK-PYTHON-IPPCRYPTO-5518127'
if re.match(pattern, url2):
    if re.match(pattern2, url2):
        print('dedededede')

import datetime

item = '2023-05-18T13:02:31+00:00'
date_obj = datetime.datetime.strptime(item, "%Y-%m-%dT%H:%M:%S%z")
# date_obj = datetime.datetime.strptime(item, "%Y-%m-%d")
print(type(date_obj))
li = []
for i in range(135, 135 + 10):
    li.append(i)
print(li)

# import requests
# import random
#
# http_ip = [
#     '65.108.147.104:8080'
# ]
# ip_proxy = random.choice(http_ip)
# proxy_ip = {
#     'http': ip_proxy,
#     'https': ip_proxy,
# }
# requese = requests.get('https://www.exploit-db.com/exploits/1515', proxies=proxy_ip).text
# print(requese)

import requests


def proxies_data1(
        # geturl='http://demo.spiderpy.cn/get/'):
        geturl='http://192.168.80.12:5010/get/'):
    try:
        proxy_data = requests.get(
            url=geturl)
        proxy_list = []
        proxy = proxy_data.json()
        proxy_list.append(proxy["proxy"])
    except:
        return "请检查环境是否启动"

    return proxy_list


print(proxies_data1())

l = [1, 2, 3]
if 4 in l:
    print(l)

import os

import sys

# 运行目录

CurrentPath = os.getcwd()

print(CurrentPath)

print(os.path)

print(len('01cbda86a304df95ec77e29ceed11ed0'))

"""_octo=GH1.1.1810419778.1683798357; _device_id=fd88b8ec2309dd72fc933b6f9fba1cec; 
user_session=4TeaaBugQ2oVklRlIE4COUcZRfk5ZUgLN38xGgfojkdRzu0b; 
__Host-user_session_same_site=4TeaaBugQ2oVklRlIE4COUcZRfk5ZUgLN38xGgfojkdRzu0b; 
logged_in=yes; dotcom_user=bobolehe; has_recent_activity=1; color_mode={"color_mode":"auto","light_theme":{"name":"light","color_mode":"light"},"dark_theme":{"name":"dark","color_mode":"dark"}}; preferred_color_mode=light; tz=Asia/Shanghai; fileTreeExpanded=true; _gh_sess=0OyHruQDgPTKAyyQxj0o7NEAOTa8/X4n5W+J2BabA2I4Z+2WoU4N/NcNJqFWuqKcQkkfKHQocPmycE6l/smrRiTpyI2HXeuRXtd6jfEsMxSZa0kB8666JYr/74kP4Ok/GxugiRiBNb3ZT+DBqVTZAaw4ai8xsGHV1yYy3fNCTrif/FUzrVkgOLRbNryPcY50Ms2x21VAVQTaAFnMQd7fJ5hTvYNE8kXsyRs/1srsP8y3CxWIGbzSxSTVGmhktp0XIA2staTckOIMpdqacMtm180hXZRNGTei6Bt1OAbyPLtYnqB5ErcZHMk=--7nC8Jv4vFkAfdCtq--9leTkDDa/EYeJgndFSictg=="""

data = '120649.json'
if 'json' in data:
    print(data)

data_dict = {"cvss2": 123, "cvss3.2": 456, "cvss3.3": 456}
print(data_dict.get('cvss3'))