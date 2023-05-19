from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

pro = '113.229.5.128:64256'
# 创建代理对象
proxy = Proxy()

# 配置代理服务器地址和端口
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = 'http://' + pro
proxy.ssl_proxy = 'http://' + pro

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
# 将代理配置应用到ChromeOptions
chrome_options.add_argument('--proxy-server={}'.format(proxy.http_proxy))

bro = webdriver.Chrome(executable_path="chromedriver", options=chrome_options)
bro.get("https://serviceexpress.com/resources/eol-eosl-database/?start=-90&timespan=90")
page_text = bro.page_source
