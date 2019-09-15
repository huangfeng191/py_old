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

import misc.reuse  as reuse

dynamic_comm_test = comm.CRUD(ctx.dynamicdb, "test", [("method", 1)])
dynamic_comm_test_log = comm.CRUD(ctx.dynamicdb, "test_log", [("method", 1)])

dynamic_daily_business= comm.CRUD(ctx.dynamicdb, "daily_business", [("method", 1)])




#  将参数 组合成需要的 格式 ， 配置与方法的转换
def dynamic_params_wrapper(func):
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
        q = {}
        for k, v in queries.items():
            if k not in q:
                q[k] = {}
            if  isinstance(v,basestring) or not v.get("type") or v.get("type") == "normal":
                q[k] = v
            elif v.get("type") == "date":
                if v.get("value") and params["date"] and params["date"][v.get("value")]:
                    val = params["date"][v.get("value")]
                    q[k] = {"$" + v.get("operate", "eq"): val}
            elif v.get("type") == "log":
                if v.get("field"):
                    logSource=kwArgs.get("logSource")
                    one = eval(logSource).get({"outFrequency": log.get("outFrequency"), "sn": v.get("sn")})
                    if one and one.get("data"):
                        q[k] = {"$"+v.get("operate","in"): one.get("data") [v.get("field")]}

                pass
        return q

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
            p["source"]=bindSource(source)

        if "queries" in kwArgs:  # 参数时需要规则，比如重用规则
            p["queries"]=bindQueries(**kwArgs)

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

