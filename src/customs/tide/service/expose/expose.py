# -*- coding: UTF-8 -*-
# Module  : py
# Description :对外提供的方法及对象
# Author  : Wujj
# Date    : 2020/2/19
# Version : 1.0

from  customs.tide.service.gather.chain import  *
from  customs.tide.service.gather.layer import  *
from customs.tide.service.dual.rule.doing import *
class TaskRun:
    def __init__(self,hookId,hook):
        self.hook=hook
        self.hookId=hookId
        self.o_chains=Chains(hookId,hook )
    def doChain(self,chain):
        o_chain = Chain(chain)
        cell_layer = o_chain.getLayer("cell")
        o_layer = Layer(cell_layer)


        kw={
            "chain":o_chain,
            "cell_layer":o_layer,
        }
        task=CellDoing(**kw)
        return task.go()


    def go(self):
        chains = self.o_chains.get()
        for chain in  chains:
           ret=self.doChain(chain)
           print "OK"
