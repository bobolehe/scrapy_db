import requests
import random


class GetProxy:

    def proxies_data1(self, geturl='http://192.168.80.12:5010/all/', target_url="https://cxsecurity.com/exploit/1"):
        try:
            proxy_data = requests.get(
                url=geturl)
            proxy_list = []
            proxy = proxy_data.json()
            for pro in proxy:
                proxy_list.append(pro["proxy"])

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }
            yx_list = []
            for proxy in proxy_list:
                try:
                    proxies = {
                        'http': proxy,
                        'https': proxy
                    }
                    response = requests.get(target_url, headers=headers, proxies=proxies, timeout=10)

                except Exception as e:
                    print(f"请求失败，代理IP无效")
                else:
                    yx_list.append(proxy)
                    print("请求成功，代理IP有效！")
            return yx_list
        except:
            return "请检查环境是否启动"

    def run(self, target_url):
        proxy_list = self.proxies_data1(target_url=target_url)
        return proxy_list


if __name__ == '__main__':
    h = GetProxy()
    print(h.run(target_url="https://cxsecurity.com/exploit/1"))
