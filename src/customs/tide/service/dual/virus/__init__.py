# -*- coding: UTF-8 -*-
# Module  : py
# Description : 将 rule 后的对象 扩散开来
# Author  : Wujj
# Date    : 2020/2/16
# Version : 1.0
from customs.tide.service.gather.chain import *
from customs.tide.service.utils import *
from customs.tide.service.persistence import *
class ContactVirus:

    def __init__(self, chain, nextChain, cell_layer):
        self.chain= chain
        self.nextChain= nextChain
        self.cell_layer = cell_layer
        self.RNA = {}
        for s in ["take"]:
            self.RNA[s]=cell_layer.get(s)



    def getInfectHook(self):
        '''
            获取 RNA 的最长扩散路径
        Returns:

        '''
        cursor = self.chain.get()
        next =self.nextChain.get() if  self.nextChain else  None
        infect=cursor.get("topHook")
        if next:
            while infect:
                layer_cursor = cursor.get(infect)
                layer_next = next.get(infect)
                if equalObj(layer_cursor.get("fetch").get("key"),layer_next.get("fetch").get("key")):
                    layer=self.chain.getChildLayer(infect)
                    if layer:
                        infect= layer.get("hook")
                else:
                    infect=layer_cursor.get("hook")
                    break
        return infect

    def doLog(self,hook,data):
        return doTideLog(hook,data)




    def spread(self):
        RNA = self.RNA
        infect=self.getInfectHook()
        while True:
            data=self.chain.getLayer(infect)
            data.update(**RNA)
            self.doLog(infect,data)
            infect=getChildLevel(infect)
            if not infect:
                break
