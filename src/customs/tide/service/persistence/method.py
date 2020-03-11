# -*- coding: UTF-8 -*-
# Module  : py
# Description :rule 可以调用的方法 
# Author  : Wujj
# Date    : 2020/2/11
# Version : 1.0



from customs.stock.service.tushare_beans import *
from customs.tide.service.utils import *
from customs.tide.service.bean.base import *
from customs.tide.service.bean.out import *

rule_doing_methods=[("table",{}),("aggregate",{})]


# rule_doing_(ruleType)
def rule_doing_table(table,rule={}):

    arrange={}
    if table.get("query"):
        arrange["query"]=compressObject(table.get("query"))
    if rule:
        for s in ["query","sorts","limits"]:
            if s=="query":
                q=compressObject(rule.get("query",{}))
                arrange[s].update(q)
            elif s=="limits":
                arrange["size"]=rule.get("limits",{}).get("size")

            elif s=="sorts":
                arrange["order"]=rule.get("sorts",{}).get("order")
    ret = None
    if(table and table.get("nm")):
        l=eval(table.get("nm")).items(**arrange)
        ret=list(l)
    return ret


def rule_doing_aggregate(table,rule=[]):
    ectype=[]+rule
    ret = None
    if (table and table.get("nm")):
        if (table and table.get("query")): # 合并查询条件
            ectype.insert(0, {"$match": table.get("query")})
        d = eval(table.get("nm")).db.aggregate(ectype)
        ret = list(d)
        # 将 数据组成 同一级对象
        for r in ret:
            if r["_id"]:
                r.update(r["_id"])
                del r["_id"]
    return ret





def save_data(table,data,key):
    l=data
    if type(data)==dict:
        l=[data]
    else:
        for r in l:
            r["key"]=key
            eval(table.get("nm")).upsert(**r)


class TileOut:
    def __init__(self,tableNm,hook):

        self.module = eval("%s_%s" % (tableNm, hook))

    def one(self,query):
        return self.module.one(query=query)