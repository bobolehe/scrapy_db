import json
import requests
import random


class GetProxy:

    def proxies_data(self,
                     geturl='http://zltiqu.pyhttp.taolop.com/getip?count=1&neek=70007&type=2&yys=0&port=2&sb=&mr=1&sep=0'):
        try:
            proxy_data = requests.get(url=geturl)
            proxy_list = []
            for proxy in proxy_data.json()['data']:
                proxy_list.append(proxy['ip'] + ':' + str(proxy['port']))
        except:
            return "请检查环境是否启动"

        return proxy_list


if __name__ == '__main__':
    h = GetProxy()
    print(h.proxies_data())
