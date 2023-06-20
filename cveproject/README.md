爬取目标https://github.com/CVEProject/cvelist/tree-commit-info/master

需要修改请求头 request.headers['Accept'] = 'application/json'

首次请求获取到json数据

其中有github每一个文件的信息,通过键和url进行拼接。

请求获取这个文件下的文件内容

循环执行到为json结尾的文件名时，使用https://raw.githubusercontent.com/CVEProject/cvelist进行拼接url

跳转到解析json数据方法中，将json的数据提取到item对象中进行存储