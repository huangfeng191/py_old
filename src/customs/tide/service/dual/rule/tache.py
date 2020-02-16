# -*- coding: UTF-8 -*-
# Module  : py
# Description :与cell 配置有关的 对象
# Author  : Wujj
# Date    : 2020/2/16
# Version : 1.0

class CellLoopConfig:
    def __init__(self,loopType,loopConfig):
        pass
    def parse(self):
        pass
    def getCellLoop(self):
        pass
        # return array

class CellRuleConfig:
    def __init__(self,ruleType,ruleConfig):
        pass


class CellOutConfig:
    def __init__(self,outType,outConfig):
        pass

class CellSourceConfig:
    def __init__(self,sourceType,sourceConfig):
        pass


class CellDoing:
    def __init__(self,loop,source,rule,chain):
        pass

    def go(self):
        pass
#     完善 chain.cell 对象



class QueryParsed:
    '''
        field:{ type:}
                type
                    date
                    jump
                =value
    '''
    def __init__(self, type, config):
        self.type = type
        self.config = config[type]


class SourceParsed:
    # 返回对外解析的source 目前只支持 table
    def __init__(self,type,config):
        self.type=type
        self.config=config[type]

    def  get(self):
        pass



class SourceConfig:
    '''
        提供源的可获取配置, 不输出结果
        sourceType
            fixed
            jump
            slot
        sourceConfig
            fixed
                type: table
    '''
    def __init__(self,sourceType,sourceConfig):
        self.type=sourceType
        self.config=sourceConfig.get(sourceType) or None
    def getJumpData(self):
        self.config
        return {}
    def get(self):
        source=None
        if self.type =="fixed":
                source=SourceParsed(self.config["type"],self.config[self.config["type"]])
        elif self.type =="jump":
            out=self.getJumpData()
            source=SourceParsed(out["type"],out[out["type"]])
        elif self.type=="slot":
            pass






