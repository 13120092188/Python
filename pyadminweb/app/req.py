# 接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
# 账户注册：请通过该地址开通账户http://sms.ihuyi.com/register.html
 # 注意事项：
 # （1）调试期间，请用默认的模板进行测试，默认模板详见接口文档；
 # （2）请使用APIID（查看APIID请登录用户中心->验证码短信->产品总览->APIID）及 APIkey来调用接口；
 # （3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；

 # !/usr/local/bin/python
 # -*- coding:utf-8 -*-
import http.client
import urllib
import random

host = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"

# 用户名是登录用户中心->验证码短信->产品总览->APIID
account = "C70305402"
# 密码 查看密码请登录用户中心->验证码短信->产品总览->APIKEY
password = "16a1cb4b67ac1c735769782f3657e161"
global yanzheng
def send_sms(text, mobile):
    params = urllib.parse.urlencode(
        {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str



def code(mobile):
    yanzheng = random.randint(100000,999999) # 生成大于等于100000小于等于999999的一个数

    text = "您的验证码是：" + str(yanzheng) + "。请不要把验证码泄露给其他人。" # 将整型x转为字符串型并且发送
    print(send_sms(text, mobile))