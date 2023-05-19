使用python中`xml.etree.ElementTree`模块

内置模块无需下载

`xml.etree.ElementTree`模块实现了一个简单高效的API，用于解析和创建XML数据。

在ElementTreeXml中封装了解析xml格式文件方法

具体功能

| 方法               | 功能                                       | 简述                                                         |
| ------------------ | ------------------------------------------ | ------------------------------------------------------------ |
| open_xml           | 打开xml文件                                | 由于文件编码格式不同，方法内自动修改编码格式                 |
| xml_data           | 解析所有节点下的内容                       | 输出所有节点下数据，父节点 { 子节点：数据，子节点：{子节点下数据}} |
| xml_attribute_data | 解析所有节点下的参数（属性、内容、子节点） | 数据格式：<br />{遍历标签序号：{标签名称：{标签序号：[             <br />              {标签所有的属性},            <br />              {遍历标签下标签序号：{标签名称：{标签序号：[                     <br />                                         {标签所有的属性},                    <br />                                         {遍历标签下的标签},                     <br />                                         {标签中的内容}]}}},            <br />              {标签中的内容}]}}} |
|                    |                                            |                                                              |

使用方法：先使用open_xml方法打开文件，返回`ElementTree`对象,使用解析方法传递`ElementTree`对象，方法执行，返回解析后的数据为字典格式
