# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/2/11
# Version : 1.0

import method



class BindQuery:
    def __init__(self,ruleType,query):
        query={
            "sn":"",
            "t":{
                "type":"date",
                "likely":"cycle" # cycle  day month week year
            },
            "trade_date":{
                "type":"jump",
                "hook":"cell",
                "fetch":{
                    "sn":"cell_last7days",
                    "cycle": "day",
                    "t": "" ,
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






class  RuleDoing:
    '''
    rule 只用到 两个 参数 ruleType  ruleConfig
    '''
    def __init__(self,ruleType,ruleConfig):

        self.ruleType = ruleType
        self.config = (json.loads(ruleConfig) or {}).get(ruleType)

    def parseConfig(self):
        pass
        query=self.config.get("query")
    def go(self):
        for s,_ in rule_doing_methods:
            if s == self.ruleType:
                eval(contactToMethod(s,{"rule":self.rule }))