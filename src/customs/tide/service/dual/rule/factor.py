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
                        latch // 将 take 数据中 抽取符合的字段 
                             "assist":""   // if null get field 

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





class TransformRegulate:
    '''
        数据转换的规则: 单个规则 
        object:
            quote:  中的对象 字段改名 {"field1":"field2" ,"field3":"field4" }
            restrain: 提取有用的字段 ["field1","field2"...]
        array:
            extract 
                way 
                    rowsToField
                        fields:[f1,f2,f3...]



        func go(data ) start translate 
    '''
    def __init__(self,type,config):
        self.type=type
        self.config=config

    def  quote(self,o={}):
        '''
        quote ={"field1":"field2" ,"field3":"field4" }
        Args:
            o:

        Returns:

        '''
        config=self.config.get("quote")
        for k,q in config.items():
            o[k]=o[q]
            if o.has_key(q):
                del o[q]
    def restrain(self,o={}):
        '''
        restrain=["field1","field2"...]
        Args:
            o:

        Returns:

        '''
        fields = self.config.get("restrain")
        for  k,v in o.items():
            if k not in fields:
                del o[k]

    def extract(self,l):
        '''
        从数组中抽取字段变为 Obj
        Args:
            a:

        Returns:

        '''
        way=self.config.get("way")
        fields=self.config.get("fields")
        o={}
        if way=="rowsToField":
            for f in fields:
                if f not in o:
                    o[f]=[]
                for r in l:
                    o[f].append(r.get(f))

        return o




    def go(self,data=[]) :
        pass
        if type(data)=="dict":
            self[self.type](data)
        elif self.type=="extract":
            data= self[self.type](data)
        else:
            for r in data:
               self[self.type](data)
        return data
class TransformConfig:
    '''
        将数据按 配置的 数组规则进行 转换 
    '''
    def __init__(self,config):
        '''
            config =[oneConfig,]
        Args:
            config:
        '''
        self.config=config or []
    def go(self,data):
        '''
            数据转换 按数组的方式应用规则
        Args:
            data:

        Returns:

        '''
        for r in self.config:
            oneRegulate=TransformRegulate(r.get("type"))
            data=oneRegulate.go(data)
        return data


class OutParsed:
    def __init__(self,type,config,layer):
        self.type=type
        self.config=config
        self.table={}
        if(type=="log"):
            self.table["nm"]="cell_log"
        else:
            self.table["nm"] = config.get("table")["nm"]

    def restrain(self,o):
        fields=self.config.get("fields")
        for  k,v in o.items():
            if k not in fields:
                del o[k]


    def getData(self,data):
        self[self.config](data)
        l=data
        if type=="log":
            l=[data]
        for r in l:
            self.restrain(r)
        return data
    def getTable(self):
        return self.table 


