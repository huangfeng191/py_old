# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/2/5
# Version : 1.0
# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/2/5
# Version : 1.0

import misc.utils as utils
import time

import json

def getCycleToT(cycle,t=None):
    '''
    Args:
        cycle:  day month year week
        s:  str 字符串时间 ，None 是 现在

    Returns:

    '''
    o={
        "day":"%Y%m%d",
        "month":"%Y%m",
        "year":"%Y"
    }

    if not t:
        ti =int(time.time())
        if cycle =="week":
            t,_=utils.getFirstEndDayOfWeek(ti)
        else:
            t=utils.YMD(ti,o[cycle])
    return t

def contactToMethod(str,params={}):
    '''

    Args:
        str:  方法名
        params: 方法的 Object 参数

    Returns:
        待 eval 的 string 方法
    '''
    s=(str+"(**%s)")%json.dumps(params)
    return  s




def compressObject(obj):
    '''
    #  将多级object 对象 压缩成  一级用 . 区分的对象
    Args:
        obj: {"a":1,"b":{"c":1}}

    Returns:
        {"a":1,"b.c":1}

    '''
    def plusKey(base, key, val, compressed):
        base1 = base + key
        if type(val) == dict and len(val.keys()) > 0:
            base1 = base1 + "."
            for k, v in val.items():
                plusKey(base1, k, v, compressed)

        else:
            compressed[base1] = val

    o = {}
    base = ""
    compressed = {}
    for k, v in obj.items():
        plusKey(base, k, v, compressed)

    return compressed