# -*- coding: UTF-8 -*-
# Module  : py
# Description :请求
# Author  : Wujj
# Date    : 2018/07/10
# Version : 1.0
import requests

"""
get 请求

 """

r = requests.get('https://www.douban.com/')
# 状态码
print r.status_code
# 内容
# 无论响应是文本还是二进制内容，我们都可以用content属性获得bytes对象：
print r.content
print r.encoding
""" 
params  dict
 """
def getUrl(url,param):
    r = requests.get(url, params=param)
    if r.status_code==200:
        return r.content
    else:
        return ""





def toPostUrl(url,params={}):
    # data 传入 是一个 string
    # requests默认使用application/x-www-form-urlencoded对POST数据编码
    # 如果要用json 方式 就 把data 改成json 就好了
    r = requests.post(url=url, data=params)
    if r.status_code==200:
        return r.content
    else:
        return ""