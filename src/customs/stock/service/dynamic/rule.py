# -*- coding: UTF-8 -*-
# Module  : py
# Description :设置算法
# Author  : Wujj
# Date    : 2019/09/01
# Version : 1.0

import misc.reuse  as reuse
import misc.wrapper as wrapper
from customs.stock.service.tushare_beans import *
from customs.stock.service.dynamic.comm import *

# 从对象中找出需要的字段
def getFieldsFilter(row,fields):
    one={}
    for field in fields:
        one[field]=row[field]
    return one




# 将参数转换 写成规则
# a={"type":"last",
#     "option":{
#         "source":{"table":"cal_date"},
#         "limit":{"rows":7 },
#         "queries":{
#             "cal_date":{"type":"date","value":"day","operate":"gte"}
#         },
#         "out":{
#             "type":"array" # object  has key
#             "fields":[],
#             "key":""
#         }
#     }
# }
# params { "date":{"day"... "month" } }






@wrapper.dynamic_params_wrapper
def dynamicQuery(source,queries,limits,sorts,params=None,*args,**kwArgs):
    d=None
    if(source and source.get("table")):
        d=eval(source.get("table")).items(query=queries,
                          order=sorts.get("order"),
                          size=limits.get("size") )
        d=list(d)
    return d



# last



def getLastResult(source={},  out={}, **kwargs):

    d = []  # 记录

    if source: # 获取数据
        d = dynamicQuery(source,**kwargs)
    if "log" in kwargs:
        dynamic_comm_test_log.upsert(**kwargs["log"])

    prep = out.get(out.get("type","log"))
    if out.get("type")=="log": #priority : field > fields 返回值 放在data 的 key 对应的字段里
        if prep.get("field"):
            d = [r.get(prep.get("field")) for r in d]
        elif   prep.get("fields"):
            d = [getFieldsFilter(r, out.get("fields")) for r in d]
    ret= None   # 对于保存在 日志表里的记录， 可以理解为 是 object
    if out.get("type") in ["log" ,"object"]  :
        ret = {prep.get("key"): d}
        if  out.get("type") =="log":
            if "data" not in kwargs["log"]:
                kwargs["log"]["data"] = {}
            kwargs["log"]["data"].update(ret)
        dynamic_comm_test_log.upsert(**kwargs["log"])


    elif out.get("type") in ["array"]: # 一般用于中间输出
        ret = d;
    else:
        pass
    return ret