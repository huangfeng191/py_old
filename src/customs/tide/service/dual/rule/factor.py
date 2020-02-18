# -*- coding: UTF-8 -*-
# Module  : py
# Description :中间对象
# Author  : Wujj
# Date    : 2020/2/17
# Version : 1.0
from customs.tide.service.utils import * 

class QueryParsed:
    '''
     一般理解是 table 的 查询
            field:value
            field:
                type  # 可以计算得到 value
                    cycle
                        extend
                        day
                        week
                        month
                        year
                    jump
                        hook
                        fetchKey
                            take
                                table  // 1条记录
                        latch
                             "assist":""

                value
                operate
                    "lte" ...

    '''
    def __init__(self,  config,layer,**kwargs):

        self.config = config or {}
        self.layer=layer
    def parseTypeDate(self,restrain,**kwargs):
        t="";
        if restrain=="cycle":
            t=self.layer.get("fetch").get("key").get("t")
        else:
            t=getCycleToT(restrain)
        return t
    def parseTypeJump(self,hook,fetchKey,latch ,**kwargs):
        pass

    def praseOperate(self):
        pass
    def get(self):
        conditions=[]
        q={

        }
        for k,v in self.config.items():
            condition = {
                "field": k,
                "operate": "=",
                "value": v
            }
            if type(v) == dict and v.get("type"):
                condition.update(v)   # 取配置值
                value=None
                if v.get("type")=="date":
                    value=self.parseTypeDate(**v)
                elif v.get("type")=="jump":
                    value = self.parseTypeJump(**v)
                condition["value"]=value
                conditions.append(condition)
            else:
                q[k]=v
        q_c=parseConditions(conditions)
        if q_c.get("$and"):
            q.update(q_c.get("$and",{}))
        return q


class SourceParsed:
    '''
    type
        table

    config
        nm
        query
            field:value
            field:
                type
                    date
                    jump

    '''
    def __init__(self,type,config,layer,**kwargs):
        self.type=type
        self.config=config[type]
        self.layer=layer

    def  get(self):
        source={"type":self.type}
        if self.type=="table":
            table={}
            table.update(self.config)
            QP=QueryParsed(self.config.get("query"),self.layer)
            table["query"]=QP.get()
            source[self.type]=table
        return source

