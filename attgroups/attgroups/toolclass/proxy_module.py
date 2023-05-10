import requests


class GetProxy:
    def proxies_data(self,
                     # geturl='http://demo.spiderpy.cn/get/'):
                     geturl='http://127.0.0.1:5432/all/'):
        try:
            proxy_data = requests.get(
                url=geturl)
            proxy_list = []
            for proxy in proxy_data.json():
                proxy_list.append(proxy["proxy"])
        except:
            return "请检查环境是否启动"
        else:
            return proxy_list


if __name__ == '__main__':
    h = GetProxy()
    print(h.proxies_data())
