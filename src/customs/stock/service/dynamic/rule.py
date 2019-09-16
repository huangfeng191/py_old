# -*- coding: UTF-8 -*-
# Module  : py
# Description :设置算法
# Author  : Wujj
# Date    : 2019/09/01
# Version : 1.0

import misc.reuse  as reuse
import misc.wrapper as wrapper
from customs.stock.service.tushare_beans import *
from customs.stock.service.dynamic import *
from customs.stock.service.dynamic.common import *

from copy import deepcopy
import json





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






@dynamic_params_wrapper
def dynamicQuery(source,queries,limits,sorts,params=None,*args,**kwArgs):
    d=None
    if(source and source.get("table")):
        d=eval(source.get("table")).items(query=queries,
                          order=sorts.get("order"),
                          size=limits.get("size") )
        d=list(d)
    return d



# last

# 要把 key 也加上去

def getLastResult(source={},  out={}, **kwargs):

    d = []  # 记录

    if source: # 获取数据
        d = dynamicQuery(source,**kwargs)

    dealwithOut(out,d,**kwargs)


def dealwithOut(out,d,log,**kwArgs):
    logSource = kwArgs.get("logSource")
    prep = out.get(out.get("type", "log"))
    if out.get("type") == "log" and logSource:  # priority : field > fields 返回值 放在data 的 key 对应的字段里
        eval(logSource).upsert(**log)
        if prep.get("field"):
            d = [r.get(prep.get("field")) for r in d]
        elif prep.get("fields"):
            d = [getFieldsFilter(r, out.get("fields")) for r in d]
    ret = None  # 对于保存在 日志表里的记录， 可以理解为 是 object
    if out.get("type") in ["log", "object"]:
        ret = {prep.get("key"): d}
        if out.get("type") == "log":
            if "data" not in log:
                log["data"] = {}
            log["data"].update(ret)
        eval(logSource).upsert(**log)
    elif out.get("type")=="table":

        # "table": {
        #     "nm": "dynamic_daily_business",
        #     "key": {
        #         "sn": 1,
        #         "outFrequency": 1
        #     }
        # }

        config=out.get("table")
        old_queries={}
        for k,v in config.get("key").items():
            if( k in log):
                old_queries[k]=log.get(k)
        eval(config.get("nm")).delete(old_queries, multi=True)
        for r in d:
            r.update(old_queries)
            eval(config.get("nm")).upsert(**r)




        pass

    elif out.get("type") in ["array"]:  # 一般用于中间输出
        ret = d;
    else:
        pass
    return ret



# 后续可以考虑 如果是 first 的时会 把原来的记录返回
# bind 后续的 规则是否生成 ，还是获取

def bind_outGenerate_wrapper(func):
    def wrap( **cell):
        sn= cell.get("sn")
        outType =cell.get("outType")
        frequency=cell.get("frequency")
        outGenerate=cell.get("outGenerate")
        logSource=cell.get("logSource")
        one=deepcopy(cell)
        one["bid"]=one["_id"]
        del one["_id"]
        if outType == "log":
            if (frequency):
                outFrequency = reuse.getFrequencyStart(frequency)
                one["outFrequency"]=outFrequency
                old = eval(logSource).get({ "outFrequency": outFrequency, "sn": sn})
                if old:
                    if outGenerate == "first":
                        pass
                    else:
                        one["_id"]=old["_id"]

        for s in ["rule","reuseParams","out"]:
            if one[s]:
                cell[s]=json.loads(one[s] )
        log = eval(logSource).upsert(**one)
        kwArgs = cell["rule"]
        kwArgs["out"]=cell["out"]
        kwArgs["params"]=cell.get("reuseParams") # 公共参数
        kwArgs["log"]=log # 日志
        kwArgs["logSource"]=logSource
        kwArgs["out"]["type"]=one.get("outType")
        kwArgs["ruleType"]=log.get("ruleType")
        res = func(**kwArgs)

        return res

    return wrap

