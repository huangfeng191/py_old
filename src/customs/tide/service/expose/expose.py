# -*- coding: UTF-8 -*-
# Module  : py
# Description :对外提供的方法及对象
# Author  : Wujj
# Date    : 2020/2/19
# Version : 1.0

from  customs.tide.service.gather.chain import  *
from  customs.tide.service.gather.layer import  *
from customs.tide.service.dual.rule.doing import *
from customs.tide.service.dual.virus import *
class TaskRun:
    def __init__(self,hookId,hook):
        self.hook=hook
        self.hookId=hookId
        self.o_chains=Chains(hookId,hook )
    def doChain(self,chain,nextChain=None):
        o_chain = Chain(chain)
        o_nextChain=None
        if nextChain:
            o_nextChain=Chain(nextChain)
        cell_layer = o_chain.getLayer("cell")
        o_layer = Layer(cell_layer)


        kw={
            "chain":o_chain,
            "cell_layer":o_layer,
        }
        task=CellDoing(**kw)
        # 保存cell 数据,返回获取输出的获取配置
        task.go()
        layer=task.getLayer()
        # out 里面有 take
        # 计入日志
        C = ContactVirus(chain, o_nextChain,layer.get("take"))
        C.spread()
        return layer


    def go(self):
        chains = self.o_chains.get()
        for i in range(0,len(chains)):
            chain=chains[i]
            ret=self.doChain(chain,(chains[i + 1] or None))

            print "OK"
