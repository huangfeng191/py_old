# -*- coding: UTF-8 -*-
# Module  : py
# Description :设置算法
# Author  : Wujj
# Date    : 2019/09/01
# Version : 1.0

import misc.reuse  as reuse
from customs.stock.service.tushare_beans import *

# 从对象中找出需要的字段
def getFieldsFilter(row,fields):
    one={}
    for field in fields:
        one[field]=row[field]
    return one




# last

# {"type":"last",
#     "option":{
#   source
#                   "limit":{"rows":7 }
#                   "queries":{
#                       "cal_date":"today"
#                       }
#                    },
#                     "out":{
#     "type":"array" object
#                         "fields":[],
#                         "key":""
#                      }
#
#                }
#  table 说明 取自记录表
def  getLastResult(source={},queries={},sorts={},limits={},out={},params={},**kwargs):


     d=[]# 记录

     if source:
        d=dynamicQuery(source,queries,limits,sorts,params)

     if(out.get("fields")) and len(d)>0:
         d=[  getFieldsFilter(r,out.get("fields"))   for  r in d ]
     elif(out.get("field")):
         d=[r.get(out.get("field")) for r in d ]

     if out.get("type")=="object":
         return {out.get("key"):d}
     if out.get("type")=="array":
         return d ;
     else :
         pass


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


def dynamicQuery(source,queries,limits,sorts,params=None):


    #   today month year
    def bindSource(source):
        table=None
        if source.get("table") :
            table = source.get("table")
        return {
            "table":table
        }


    def bindQueries(queries={}, reuse={}):
        q = {}
        for k, v in queries.items():
            if k not in q:
                q[k] = {}
            if not v.get("type") or v.get("type") == "normal":
                q[k]["$" + v.get("operate", "eq")] = v.get("value")
            elif v.get("type") == "date":
                if v.get("value") and reuse["date"] and reuse["date"][v.get("value")]:
                    val = reuse["date"][v.get("value")]
                    q[k] = {"$" + v.get("operate", "eq"): val}
        return q

    # "limit":{"rows":7 },
    def bindLimits(limits={}):
        size = None
        if limits.get("rows"):
            size= limits.get("rows")
        return size

    def bindSorts(sorts):
        if "order" in sorts and sorts.get("order"):
            return sorts.get("order")
        # if( "_sort" in sorts) and sorts.get("_sort"):
        #         return []
        return None
    # start
    sour=bindSource(source)
    d=None
    if(sour.get("table")):
        d=eval(sour.get("table")).items(query=bindQueries(queries,
                                                          reuse.bindReuse(params)),
                          order=bindSorts(sorts),
                          size=bindLimits(limits), )
        d=list(d)
    return d

