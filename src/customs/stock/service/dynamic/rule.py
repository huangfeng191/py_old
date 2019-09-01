# -*- coding: UTF-8 -*-
# Module  : py
# Description :设置算法
# Author  : Wujj
# Date    : 2019/09/01
# Version : 1.0



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
def  getLastResult(source={},queries={},sort={},limits={},out={}):


     limit=None
     d=[]# 记录
     if limits.get("row"):
         limit=limits.get("row")
     if source.get("type")=="table":
        table=source.get("table")
        d=eval(table).items(query=queries,sort=sort,limit=limit)
     if(out.get("fields")) and d.length>0:
         d=map(getFieldsFilter,d)
     if out.get("type")=="object":
         return {out.get("key"):d}
     if out.get("type")=="array":
         return d ;
     else :
         pass


