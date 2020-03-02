# -*- coding: UTF-8 -*-
# Module  : py
# Description :rule 可以调用的方法 
# Author  : Wujj
# Date    : 2020/2/11
# Version : 1.0



from customs.stock.service.tushare_beans import *
from customs.tide.service.utils import *
from customs.tide.service.bean.base import *

rule_doing_methods=[("table",{}),("agg",{})]


# rule_doing_(ruleType)
def rule_doing_table(table,rule={}):

    arrange={}
    if table.get("query"):
        arrange["query"]=compressObject(table.get("query"))
    if rule:
        for s in ["query","sorts","limits"]:
            if s=="query":
                arrange[s].update(**rule.get("query",{}))
            elif s=="limits":
                arrange["size"]=rule.get("limits",{}).get("size")

            elif s=="sorts":
                arrange["order"]=rule.get("sorts",{}).get("order")
    ret = None
    if(table and table.get("nm")):
        l=eval(table.get("nm")).items(**arrange)
        ret=list(l)
    return ret


def rule_doing_aggregate(table,rule):
    table={
        "nm":"",
        "query":""
    }

    ret = None
    if (table and table.get("nm")):
        if (table and table.get("query")): # 合并查询条件
            rule.insert(0, {"$match": table.get("query")})
        d = eval(table.get("nm")).db.aggregate(rule)
        ret = list(d)
        # 将 数据组成 同一级对象
        for r in d:
            r.update(r["_id"])
    return ret





def save_data(table,data,key):
    l=data
    if type(data)==dict:
        l=[data]
    else:
        for r in l:
            r["key"]=key
            eval(table.get("nm")).upsert(**r)
