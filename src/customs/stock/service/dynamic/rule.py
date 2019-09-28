# -*- coding: UTF-8 -*-
# Module  : py
# Description :设置算法
# Author  : Wujj
# Date    : 2019/09/01
# Version : 1.0

import misc.reuse  as reuse
import misc.wrapper as wrapper
from customs.stock.service.dynamic.common import *
from customs.stock.service.tushare_beans import *
from customs.stock.service.dynamic import *


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

@wrapper.calc_runtime_wrapper
@wrapper.loop_fun_reset_wrapper
@dynamic_params_wrapper
def beforeDynamicQuery(**kwArgs):
    kw =deepcopy(kwArgs)

    if(kwArgs.get("aQueries")):
        for r in kwArgs.get("aQueries"):
            kw["queries"]=r
            dynamicDeal(**kw)

        return "OK"
    else:
        return dynamicDeal(**kwArgs)





def dynamicQuery(source,queries,limits,sorts,params=None,*args,**kwArgs):
    d=None
    if(source and source.get("table")):
        d=eval(source.get("table")).items(query=queries,
                          order=sorts.get("order"),
                          size=limits.get("size") )
        d=list(d)
    return d
@wrapper.loop_fun_wrapper
def dynamicDeal(source={},  out={},**kwArgs):
    d=dynamicQuery(source,**kwArgs)
    ret=dealwithOut(out, d, **kwArgs)

    return ret


# 只有表的时候需要删除，其他的不需要
def dealWithOutClear(out,log):

    if out.get("type")=="table":
        config=out.get("table")
        old_queries={}
        for k,v in config.get("logKey",{}).items():
            if( k in log):
                old_queries[k]=log.get(k)
        eval(config.get("nm")).delete(old_queries, multi=True)


# dataKey 数据的key 一般用于 loop
# logKey 此次产生的所有数据的key
# 当 d =[] 时 可以理解为清空数据
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
        for k,v in config.get("logKey",{}).items():
            if( k in log):
                old_queries[k]=log.get(k)
        for k, v in config.get("dataKey",{}).items():
            if (k in kwArgs.get("queries",{})):
                old_queries[k] = kwArgs.get("queries").get(k)
        eval(config.get("nm")).delete(old_queries, multi=True)
        for r in d:
            if "_id" in r:
                del r["_id"]
            r.update(old_queries)
            eval(config.get("nm")).upsert(**r)

        ret="OK"



    elif out.get("type") in ["array"]:  # 一般用于中间输出
        ret = d;
    else:
        pass
    if logSource and log:
        log["logState"] = 1
        eval(logSource).upsert(**log)

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
        # if outType == "log":
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




@wrapper.calc_runtime_wrapper
@wrapper.loop_fun_reset_wrapper
@dynamic_params_wrapper
def beforeAggregateQuery(**kwArgs):
    kw =deepcopy(kwArgs)

    if(kwArgs.get("aQueries")):
        for r in kwArgs.get("aQueries"):
            kw["queries"]=r
            aggregateDeal(**kw)

        return "OK"
    else:
        return aggregateDeal(**kwArgs)



def daggregateDealQuery(source,queries,*args,**kwArgs):
    d=None
    if(source and source.get("table")):

        step=[]
        if kwArgs.get("aggregate"):
            step=kwArgs.get("aggregate")
        if (queries):
            step.insert(0,{"$match": queries})

        d = eval(source.get("table")).db.aggregate(step)
        d=list(d)
    return d
@wrapper.loop_fun_wrapper
def aggregateDeal(source={},  out={},**kwArgs):
    d=daggregateDealQuery(source,**kwArgs)
    ret=dealwithOut(out, d, **kwArgs)

    return ret



