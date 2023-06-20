import requests


class GetProxy:

    def proxies_data1(self,
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

    def proxies_data2(self,
                      # geturl='http://demo.spiderpy.cn/get/'):
                      geturl='http://zltiqu.pyhttp.taolop.com/getip?count=2&neek=70007&type=2&yys=0&port=2&sb=&mr=2&sep=0'):
        try:
            proxy_data = requests.get(
                url=geturl)
            proxy_list = []
            for proxy in proxy_data.json()['data']:
                proxy_list.append(str(proxy["ip"]) + ":" + str(proxy["port"]))
        except:
            return "请检查环境是否启动"

        return proxy_list

    def run(self):
        proxy_list = self.proxies_data1()
        return proxy_list


if __name__ == '__main__':
    h = GetProxy()
    print(h.proxies_data())
