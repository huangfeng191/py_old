# -*- coding: UTF-8 -*-
# Module  : py
# Description :与cell 配置有关的 对象
# Author  : Wujj
# Date    : 2020/2/16
# Version : 1.0

from factor import *

from  customs.tide.service import utils as tide_utils
class CellLoopConfig:
    def __init__(self, loopType, loopConfig):
        pass

    def parse(self):
        pass

    def getCellLoop(self):
        pass
        # return array


class CellRuleConfig:
    '''
        {
          "table":{
                query:{
                "is_open":1
                },

                "limits": {
                    "size": 7
                },
                "sorts": {
                    "order": [{"Field": "cal_date", "Type": true}]
                }
          },
          "agg":{

          }
        }

    '''

    def __init__(self, type, config, layer):
        self.type = type
        self.config = config.get(type) or None
        self.layer = layer

    def get(self):
        rule = {}
        if self.type == "table":
            rule.update(self.config)
            QP = QueryParsed(self.config.get("query"), self.layer)
            rule["query"] = QP.get()
        elif self.type == "agg":
            pass
        return rule


class CellOutConfig:
    def __init__(self, type, config,layer):
        self.type=type
        self.config=config
        self.layer=layer
        self.layer["take"]={
            "type":type,
            "key":layer.get("fetch").get("key")
        }
        self.layer["take"][type]={
            "hook":"cell"
        }
        self.layer["info"]={}
    def table(self):
        config = self.config["table"]
        take=self.layer["take"]
        info=self.layer["info"]
        o = take["table"]
        o["nm"]=config.get("nm")

        se = {"nm": "tide_cell", "query": o.get("key")}
        if config.get("query"):
            se["query"].update(config.get("query"))
        objBindType("table",info,se)


    def log(self):
        config=self.config["log"]
        take = self.layer["take"]
        info = self.layer["info"]
        o=take["log"]
        if config.get("field"):
            o["fields"]=[config.get("field")]
        else:
            o["fields"] = config.get("fields")
        se={"nm": "tide_cell_log","fields":o["fields"]}
        se["query"]={
            "fetch":{
                "key":take.get("key")
            }
        }
        objBindType("table", info, se)

    def accrue(self):
        if self.type:
            if(self.type=="log"):
                self.log()
            elif(self.type=="table"):
                self.table()
        else:
            raise Exception("CellOutConfig error ")
        pass
    def go(self,data):
        if self.config.get("regulates"):
             T=TransformConfig(self.config.get("regulates"))
             data=T.go(data)
        self.accrue() # 绑定 take and info
        return data



class CellSourceConfig:
    '''
        提供源的可获取配置, 不输出结果
        sourceType
            fixed
            jump
            slot
        sourceConfig
            fixed
                type: table
                table:{
                    nm:""
                    query:{}
                }
    '''

    def __init__(self, type, config, layer):
        self.type = type
        self.config = config.get(type) or None
        self.layer = layer

    def getJumpData(self):
        self.config
        return {}

    def get(self):
        '''

        Returns:
            source
                {  // 返回可配置对象的原因是 方便以后的扩展
                    "type":"table",
                    "table":{
                        query:{},
                        nm:""
                    }
                }

        '''
        source = None
        if self.type == "fixed":
            SP = SourceParsed(self.config["type"], self.config, self.layer)
            source = SP.get()
        elif self.type == "jump":
            out = self.getJumpData()
            SP = SourceParsed(out["type"], out[out["type"]], self.layer)
            source = SP.get()
        elif self.type == "slot":
            pass

        return source
