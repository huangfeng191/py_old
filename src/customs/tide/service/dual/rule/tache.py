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
