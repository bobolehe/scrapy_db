
import json
import requests
import random


class GetProxy:

    def proxies_data(self,
                     # geturl='http://demo.spiderpy.cn/get/'):
                     geturl='http://192.168.80.12:5432/all/'):
        try:
            proxy_data = requests.get(
                url=geturl)
            proxy_list = []
            for proxy in proxy_data.json():
                proxy_list.append(proxy["proxy"])
        except:
            return "请检查环境是否启动"

        return proxy_list


if __name__ == '__main__':
    h = GetProxy()
    print(h.proxies_data())
