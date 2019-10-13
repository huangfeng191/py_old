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

@wrapper.calc_runtime_wrapper("DynamicQuery ")
@wrapper.loop_fun_reset_wrapper
@dynamic_params_wrapper
def beforeDynamicQuery(**kwArgs):
    kw =deepcopy(kwArgs)

    if(kwArgs.get("aQueries")):
        for r in kwArgs.get("aQueries"):
            kw["queries"]=r
            log=dynamicDeal(**kw)

        return log
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
    ret=saveWithOut(out, d, **kwArgs)

    return ret


# 只有表的时候需要删除，其他的不需要
def saveWithOutClear(out,log):

    if out.get("type")=="table":
        config=out.get("table")
        old_queries={}
        for k,v in config.get("logKey",{}).items():
            if( k in log):
                old_queries[k]=log.get(k)
        eval(config.get("table")).delete(old_queries, multi=True)



#
def saveWithOut(out,d,**kwArgs):
    logSource = kwArgs.get("logSource")
    log=kwArgs.get("log")
    unifyParsedOut(out, log, logSource)
    parsedOut = log.get("parsedOut")
    if(parsedOut.get("type")=="log"):

        fieldKey=parsedOut.get("fieldKey")
        if parsedOut.get("field"):
            d = [r.get(parsedOut.get("field")) for r in d]
        elif parsedOut.get("fields",[]):
            d = [getFieldsFilter(r, out.get("fields")) for r in d]
        ret = {fieldKey: d}
        if out.get("type") == "log":
            if "data" not in log:
                log["data"] = {}
            log["data"].update(ret)
    elif parsedOut.get("type")=="table":
        dataQueries={}
        dataQueries.update(parsedOut.get("recordKey",{}))
        for k, v in parsedOut.get("dataKey", {}).items():
            if (k in kwArgs.get("queries", {})):
                dataQueries[k] = kwArgs.get("queries").get(k)
        eval(parsedOut.get("table")).delete(dataQueries, multi=True)
        for r in d:
            if "_id" in r:
                del r["_id"]
            r.update(dataQueries)
            eval(parsedOut.get("table")).upsert(**r)

    if logSource and log:
        log["logState"] = 1
        eval(logSource).upsert(**log)
        return log
# recordKey 记录的key 也就是 单次 cell 生成的key 
def unifyParsedOut(out,log,logSource):
    # dataKey 的作用是对多条记录再次进行分类 ,parsedOut 主要是查询用
    parsedOut = {"type":out.get("type"),"recordKey":{},"dataKey":{},"table":"","fields":[],"field":None,"fieldKey":None}
    config = out.get(out.get("type"))
    if out.get("type")=="table":
        parsedOut["table"]=config.get("table")
        parsedOut["dataKey"]=config.get("dataKey", {})
        parsedOut["fields"]=config.get("fields")
    elif out.get("type")=="log":
        parsedOut["table"]=logSource
        parsedOut["recordKey"]={"_id":log.get("_id")}
        parsedOut["field"] = config.get("field")
        parsedOut["fieldKey"] = config.get("fieldKey") if config.get("fieldKey") else config.get("field")
        parsedOut["fields"] = config.get("fields")

    #本次cell 的主键
    for k, v in config.get("logKey", {}).items():
        if (k in log):
            parsedOut["recordKey"][k] = log.get(k)


    log["parsedOut"] =  parsedOut
    return log


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




@wrapper.calc_runtime_wrapper("AggregateQuery")
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
        for r in d:
            r.update(r["_id"])
    return d
@wrapper.loop_fun_wrapper
def aggregateDeal(source={},  out={},**kwArgs):
    d=daggregateDealQuery(source,**kwArgs)
    ret=saveWithOut(out, d, **kwArgs)

    return ret



