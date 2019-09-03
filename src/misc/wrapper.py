# -*- coding: UTF-8 -*-
# Module  : py
# Description :slef reuse warpper
# Author  : Wujj
# Date    : 2019/09/03
# Version : 1.0
import reuse as reuse
import json

def calc_runtime_wrapper(func):
    import time
    def wrap(**kwArgs):
        st=time.time()
        res=func(**kwArgs)
        print "continue:%f"%(time.time()-st)
        return res
    return wrap


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

    def bindQueries(queries={}, params={}):
        params=reuse.bindReuse(params)
        q = {}
        for k, v in queries.items():
            if k not in q:
                q[k] = {}
            if not v.get("type") or v.get("type") == "normal":
                q[k]["$" + v.get("operate", "eq")] = v.get("value")
            elif v.get("type") == "date":
                if v.get("value") and params["date"] and params["date"][v.get("value")]:
                    val = params["date"][v.get("value")]
                    q[k] = {"$" + v.get("operate", "eq"): val}
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
            p["queries"]=bindQueries(kwArgs["queries"],kwArgs.get("params",{}))

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




# test instance 
@calc_runtime_wrapper
def run_times(**kwArgs):
    print "OK"




