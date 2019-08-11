# -*- coding: UTF-8 -*-
# Module  : py
# Description :请求
# Author  : Wujj
# Date    : 2018/07/10
# Version : 1.0
import requests
import json

""" 
params  dict
 """
def toGetUrl(url,params={}):
    r = requests.get(url=url, params=params)
    if r.status_code==200:
        return r.content
    else:
        return ""


def toPostUrl(url,params={},**kwargs):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        "Accept": "application/json"}
    if "contentType" in kwargs:
        headers['Content-Type']=kwargs["contentType"]
    r = requests.post(url=url,headers=headers, json=params)
    if r.status_code==200:
        return {
            "status":"OK",
            "data":json.loads(r.content)
        }
    else:
        return {
            "status":"Err",
            "data":r.content
        }