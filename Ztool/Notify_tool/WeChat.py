import requests
import json


class WXWork_SMS:
    # Markdown类型消息
    def send_msg_markdown(self, content):
        headers = {"Content-Type": "text/plain"}
        send_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=84e6def8-5687-4929-a74e-c8f70d757480"
        send_data = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                'content': content
                # "content": "# **spider程序状态通知**<font color=\"warning\">**123例**</font>\n" +  # 标题 （支持1至6级标题，注意#与文字中间要有空格）
                #            # "#### **请相关同事注意，及时跟进！**\n" +  # 加粗：**需要加粗的字**
                #            "> 类型：<font color=\"info\">用户反馈</font> \n" +  # 引用：> 需要引用的文字
                #            "> 普通用户反馈：<font color=\"warning\">117例</font> \n" +  # 字体颜色(只支持3种内置颜色)
                #            "> VIP用户反馈：<font color=\"warning\">6例</font>"  # 绿色：info、灰色：comment、橙红：warning
            }
        }

        res = requests.post(url=send_url, headers=headers, json=send_data)
        print(res.text)


if __name__ == '__main__':
    sms = WXWork_SMS()
    # "#### **请相关同事注意，及时跟进！**\n" +  # 加粗：**需要加粗的字**
    # 标题 （支持1至6级标题，注意#与文字中间要有空格）
    # 引用：> 需要引用的文字
    # 字体颜色(只支持3种内置颜色)
    # 绿色：info、灰色：comment、橙红：warning
    content = "# **spider程序状态通知**<font color=\"warning\">**123例**</font>\n" \
              "> 类型：<font color=\"info\">用户反馈</font> \n" \
              "> 普通用户反馈：<font color=\"warning\">117例</font> \n" \
              "> VIP用户反馈：<font color=\"warning\">6例</font>"
    # Markdown类型消息
    sms.send_msg_markdown(content=content)
