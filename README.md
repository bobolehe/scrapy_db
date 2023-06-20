## 开发环境

​    python开发环境为3.10
​    第三方库依赖批量安装requirements.txt文件即可

​	豆瓣源 https://pypi.douban.com/simple/

scrapy不同系统环境的安装方式不同：
```
mac or linux系统安装只需要执行以下命令
pip install scrapy

windows系统：
需要提前安装scrapy所需库
pip install wheel
下载twisted，下载地址为http://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted
安装twisted：pip install 下载文件名称
pip install pywin32
pip install scrapy
```

### 使用方法：

1、爬虫文件夹目录下使用终端执行 scrapy crawl 爬虫文件名（爬虫文件名在同名文件下spiders文件下）
​    注：爬取时间根据数据量运行