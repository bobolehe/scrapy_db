import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import chardet


def open_xml(filename):
    """
    不同编码格式xml数据使用此方法
    :param filename: 文件路径
    :return:
    """
    # 尝试使用 utf-8 编码打开文件，如果失败，则使用 chardet 检测编码
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            xml = f.read()
    except UnicodeDecodeError:
        with open(filename, 'rb') as f:
            encoding = chardet.detect(f.read())['encoding']
        with open(filename, 'r', encoding=encoding) as f:
            xml = f.read()

    # 尝试使用检测到的编码解析文件，如果解析失败，则尝试使用 utf-8 编码解析
    try:
        # fromstring方法打开字符串格式xml，默认返回根节点对象
        child = ET.fromstring(xml)
        # print(root.tag)
        return child
    except ET.ParseError:
        try:
            child = ET.fromstring(xml.encode('utf-8'))
            return child
        except ET.ParseError:
            return '无法解析此数据'


def xml_data(label):
    """
    遍历xml文件，输出所有节点下数据，父节点 { 子节点：数据，子节点：{子节点下数据}}
    :param label: xml.etree.ElementTree打开xml对象
    :return: 返回最终数据
    """
    data_two = {}
    # 设定每个标签的数量，有重复标签时，使用{0：{数据}}的格式进行存储
    data_name_list = {}
    # 遍历每一个标签
    for i, child in enumerate(label):
        # 记录标签数据，作数据存储使用
        if child.tag in data_name_list:
            data_name_list[child.tag] += 1
        else:
            data_name_list[child.tag] = 0

        # 子标签的内容存储在列表结构中，考虑到有的为多个参数例如一个标签下有多个name标签，这样获取存储至列表，并且有顺序
        if child.tag in data_two:
            pass
        else:
            data_two[child.tag] = {}

        # 如果该标签包含子标签，则递归遍历子标签
        if len(child):
            data_two[child.tag][data_name_list[child.tag]] = xml_data(child)
        else:
            data_two[child.tag][data_name_list[child.tag]] = child.text

    return data_two


def xml_attribute_data(label):
    """
    遍历xml文件，输出所有节点下数据
    注意数据格式
    数据格式：{遍历标签序号：{标签名称：{标签序号：[
                {标签所有的属性},
                {遍历标签下标签序号：{标签名称：{标签序号：[
                        {标签所有的属性},
                        {遍历标签下的标签},
                        {标签中的内容}]}}},
                {标签中的内容}]}}}
    :param label:xml.etree.ElementTree打开xml对象
    :return:
    """

    data_two = {}
    # 设定每个标签的数量，有重复标签时，使用{0：{数据}}的格式进行存储
    data_name_list = {}
    # 遍历每一个标签
    for i, child in enumerate(label):
        # print(child.tag)
        # 记录标签数据，作数据存储使用
        if child.tag in data_name_list:
            data_name_list[child.tag] += 1
        else:
            data_name_list[child.tag] = 0
        # print(data_name_list)
        # 子标签的内容存储在列表结构中，考虑到有的为多个参数例如一个标签下有多个name标签，这样获取存储至列表，并且有顺序
        if child.tag in data_two:
            pass
        else:
            data_two[child.tag] = {}

        # 如果该标签包含子标签，则递归遍历子标签
        if len(child):
            data_two[child.tag][data_name_list[child.tag]] = [child.attrib]
            data_two[child.tag][data_name_list[child.tag]].append(xml_attribute_data(child))
            data_two[child.tag][data_name_list[child.tag]].append(child.text)
        else:
            data_two[child.tag][data_name_list[child.tag]] = [child.attrib]
            data_two[child.tag][data_name_list[child.tag]].append(None)
            data_two[child.tag][data_name_list[child.tag]].append(child.text)

    # print(labels_data[index])
    return data_two


if __name__ == '__main__':
    open_file = 'iop (1).xml'
    root = open_xml(open_file)
    print(xml_data(root))
    print("-" * 60, "结果分割线", "-" * 60)
    print(xml_attribute_data(root))

# # 读取文件并检测编码格式
# with open('file.xml', 'rb') as f:
#     encoding = chardet.detect(f.read())['encoding']
#
# tree = ET.parse(open('iop.xml', 'r', encoding='utf-8'))

# # 递归遍历所有标签方法
# # def traverse_xml(element):
# #     for child in element:
# #         # 如果该标签包含子标签，则递归遍历子标签
# #         if len(child):
# #             traverse_xml(child)
# #         else:
# #             print(child.tag, child.text)
# # # 打印所有标签内容
# # traverse_xml(root)
