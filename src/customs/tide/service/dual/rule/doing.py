# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/2/12
# Version : 1.0




from customs.tide.service.dual.rule.method import *

class BindQuery:
    def __init__(self,ruleType,query,fetch ):
        query={
            "sn":"",
            "t":{
                "type":"date",
                "likely":"cycle" # cycle  day month week year
                # cycle   fetch.t
            },
            "trade_date":{
                "type":"jump",
                "hook":"cell",
                "fetch":{
                    "sn":"cell_last7days",
                    "likely": "cycle" , # cycle  day month week year   # cycle   fetch.t
                    "level":"cell",
                    "levelSn":"cell_last7days"
                },
                "parseOut":{
                    "out":"array" , # string
# outType == "log" 时 可以取 ，  table  时  in   if  result.length==1 时 =
                    # 根据 jump 类型 生成 "operate": "in"

                    "objectToField":{
                        "field":""
                    }

                },


    #  log  or table

            }
        }
    def  getTable(self):
        pass
    def getAgg(self):
        pass

    def get(self):
        pass




class  RuleDoing:
    '''
    rule 只用到 两个 参数 ruleType  ruleConfig
    '''
    def __init__(self,ruleType,ruleConfig,fetch):

        self.ruleType = ruleType
        self.config = (json.loads(ruleConfig) or {}).get(ruleType)
        self.fetch=fetch

    def parseConfig(self):
        pass
        query=self.config.get("query")
    def go(self):
        for s,_ in rule_doing_methods:
            if s == self.ruleType:
                eval(contactToMethod(s,{"rule":self.rule }))

