# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2019/09/01
# Version : 1.0
# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2019/09/01
# Version : 1.0
import ctx
from service import comm
import json
from copy import deepcopy
import misc.reuse  as reuse

from customs.stock.service.tushare_beans import *

from customs.stock.service.dynamic import *

dynamic_comm_test = comm.CRUD(ctx.dynamicdb, "test", [("method", 1)])
dynamic_comm_test_log = comm.CRUD(ctx.dynamicdb, "test_log", [("method", 1)])

dynamic_daily_business= comm.CRUD(ctx.dynamicdb, "daily_business", [("method", 1)]) # 明细
dynamic_basic_business= comm.CRUD(ctx.dynamicdb, "basic_business", [("ts_code", 1)]) # 一个业务 一个 code 一条 汇总  outFrenquence  ts_code , result:{"business":{?}}




#  将参数 组合成需要的 格式 ， 配置与方法的转换
def dynamic_params_wrapper(func):
    #TODO:
    def seprateInType(source,inType,**kwArgs):
        log=kwArgs["log"]
        if inType=="cell":
            log["inTypeSn"]=""
            #TODO:
        if inType=="link":
            link=source["link"]
            if(link["type"]=="sn"):
                link_log=dynamic_link_log.get({"sn":link["type"],"outFrequency":log })
                if not link_log:
                    pass
                else:
                    out=link_log.get("out")
                    if out:
                        out=json.loads(out)
                        if out.get("type")=="table":
                           source["table"]=out.get("table")
                           source["table"]

    #   today month year
    def bindSource(source):
        table = None
        if source.get("table"):
            table = source.get("table")
        return {
            "table": table
        }

    def bindQueries(queries={}, params={},**kwArgs):
        params=reuse.bindReuse(params)
        log=kwArgs.get("log")
        otherQueries={}
        variable=[]
        otherQueries["variable"]=variable
        q = {}
        for k, v in queries.items():
            if k not in q:
                q[k] = {}
            if  isinstance(v,basestring) or isinstance(v,int) or  not v.get("type") or v.get("type") == "normal":
                q[k] = v
            elif v.get("type") == "date":
                if v.get("field") and params["date"] and params["date"][v.get("field")]:
                    val = params["date"][v.get("field")]
                    q[k] = {"$" + v.get("operate", "eq"): val}
            elif v.get("type") == "log":
                if v.get("field"):
                    logSource=kwArgs.get("logSource")
                    one = eval(logSource).get({"outFrequency": log.get("outFrequency"), "sn": v.get("sn"),"inTypeSn":v.get("inTypeSn","")   })
                    if one and one.get("data"):
                        q[k] = {"$"+v.get("operate","in"): one.get("data") [v.get("field")]}
            elif v.get("type")=="loop":
                # "type":"loop", "from":"stock_basic", "from_k":"ts_code", "from_q": r2.get("from_q")
                from_loop=v.get("from")
                one_com = {"queryKey": k, "type": v.get("type"), "from":{"table":from_loop.get("table"),
                                                                         "query":from_loop.get("query"),
                                                                         "field":from_loop.get("field"),
                                                                         "sorts":from_loop.get("sorts")}}
                variable.append(one_com)

                pass

        return q ,otherQueries
# 查询转换为 数组调用
    def combineQueries(must={},variable=[]):
        ret=[]
        if not variable:
            ret.append(must)
        for r_c in variable:
            if r_c.get("type") == "loop":
                from_loop = r_c.get("from")
                kwArg = {}
                if from_loop.get("sorts"):
                    kwArg=bindSorts(from_loop["sorts"])

                l = eval(from_loop.get("table")).items(query=(from_loop.get("query") or {}),fields=[from_loop.get("field" ,
                                                                                                                  r_c.get("queryKey"))], **kwArg)
                for r_l in l:
                    must[r_c.get("queryKey")] = r_l.get(from_loop.get("field"))
                    ret.append(deepcopy(must))
        return ret
    # "limit":{"rows":7 },
    def bindLimits(limits={}):
        size = None
        if limits.get("size"):
            size = limits.get("size")
        return {
            "size":size
        }

    def bindSorts(sorts):
        ret={"order":None}
        if "order" in sorts and sorts.get("order"):
            ret["order"]=sorts.get("order")

        # if( "_sort" in sorts) and sorts.get("_sort"):
        #         return []
        return ret

    def wrap(source,**kwArgs):
        p={}
        if source:
            # seprateInType(source,**kwArgs)
            p["source"]=bindSource(source)

        if "queries" in kwArgs:  # 参数时需要规则，比如重用规则
            p["queries"],p["otherQueries"]=bindQueries(**kwArgs)
            kwArgs["aQueries"] = combineQueries(p["queries"], p["otherQueries"].get("variable"))

        if "limits" in kwArgs:  # 参数时需要规则，比如重用规则
            p["limits"] = bindLimits(kwArgs["limits"])

        if "sorts" in kwArgs:  # 参数时需要规则，比如重用规则
            p["sorts"] = bindSorts(kwArgs["sorts"])
        if "log" in kwArgs:
            kwArgs["log"]["parseArgs"]=json.dumps(p)
        kwArgs.update(p)
        res = func(**kwArgs)
        return res
    return wrap

