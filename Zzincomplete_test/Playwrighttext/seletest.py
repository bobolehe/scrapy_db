from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path="chromedriver", options=chrome_options)

i = 0
while i < 2:
    js = "window.open('http://www.sogou.com')"
    driver.execute_script(js)

    driver.close()
    windows = driver.window_handles  # 获取当前所有页面句柄
    driver.switch_to.window(windows[0])  # 切换指定页面
    i += 1
