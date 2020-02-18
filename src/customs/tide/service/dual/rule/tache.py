# -*- coding: UTF-8 -*-
# Module  : py
# Description :与cell 配置有关的 对象
# Author  : Wujj
# Date    : 2020/2/16
# Version : 1.0

from factor  import *
class CellLoopConfig:
    def __init__(self,loopType,loopConfig):
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
    def __init__(self, type, config,layer):
        self.type = type
        self.config = config.get(type) or None
        self.layer=layer
    def get(self):
        rule={}
        if self.type=="table":
            rule.update(self.config)
            QP = QueryParsed(self.config.get("query"), self.layer)
            rule["query"] = QP.get()
        elif self.type=="agg":
            pass
        return rule

class CellOutConfig:
    def __init__(self,outType,outConfig):
        pass

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

    def __init__(self, type, config,layer):
        self.type = type
        self.config = config.get(type) or None
        self.layer=layer

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
            SP=SourceParsed(self.config["type"], self.config, self.layer)
            source = SP.get()
        elif self.type == "jump":
            out = self.getJumpData()
            SP = SourceParsed(out["type"], out[out["type"]],self.layer)
            source = SP.get()
        elif self.type == "slot":
            pass

        return source


class CellDoing:
    def __init__(self,loop,source,rule,chain):
        pass

    def go(self):
        pass
#     完善 chain.cell 对象
# source
# loop
# rule
# out




