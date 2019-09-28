# -*- coding: UTF-8 -*-
# Module  : py
# Description :用规则调用的方法
# Author  : Wujj
# Date    : 2019/09/25
# Version : 1.0


from customs.stock.service.dynamic.rule import *


# last

# 要把 key 也加上去

def getLastResult( **kwArgs):
    d=None
    if kwArgs.get("source"): # 获取数据
        d = beforeDynamicQuery(**kwArgs)
    return {
        "data":d,
        "log":kwArgs.get("log")
    }

# 通过聚合函数调用结果
def getAggregateResult(**kwArgs):
    d = None
    if kwArgs.get("source"):  # 获取数据
        d = beforeAggregateQuery(**kwArgs)
    return {
        "data":d,
        "log": kwArgs.get("log")
    }


@bind_outGenerate_wrapper
def loadRule(**kwArgs):
  ruleType=kwArgs.get("ruleType")
  if ruleType=="last": # 可以将方法也配置成参数
      return getLastResult(**kwArgs)
  elif ruleType=="aggregate":
      return getAggregateResult(**kwArgs)