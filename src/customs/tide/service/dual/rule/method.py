# -*- coding: UTF-8 -*-
# Module  : py
# Description :rule 可以调用的方法 
# Author  : Wujj
# Date    : 2020/2/11
# Version : 1.0



from customs.stock.service.tushare_beans import *
from customs.tide.service.utils import *


rule_doing_methods=[("table",{}),("agg",{})]


# rule_doing_(ruleType)
def rule_doing_table(source,rule):
    source={
        "table":"",
        "query":""
    }
    arrange={}
    for s in ["query","sorts","limits"]:
        arrange[s]=rule[s]
        if s=="query":
            arrange[s].update(source.get("query"))
    ret = None
    if(source and source.get("table")):
        l=eval(source.get("table")).items(**arrange)
        ret=list(l)
    return ret


def rule_doing_aggregate(source,rule):
    source={
        "table":"",
        "query":""
    }

    ret = None
    if (source and source.get("table")):
        if (source and source.get("query")): # 合并查询条件
            rule.insert(0, {"$match": source.get("query")})
        d = eval(source.get("table")).db.aggregate(rule)
        ret = list(d)
        # 将 数据组成 同一级对象
        for r in d:
            r.update(r["_id"])
    return ret

