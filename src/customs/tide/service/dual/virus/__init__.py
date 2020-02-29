# -*- coding: UTF-8 -*-
# Module  : py
# Description : 将 rule 后的对象 扩散开来
# Author  : Wujj
# Date    : 2020/2/16
# Version : 1.0
from customs.tide.service.gather.chain import *
from customs.tide.service.utils import *
class Virus:
    def __init__(self,chains,layer,outConfig):
        self.chains=chains
        self.layer=layer
        self.outConfig=outConfig
        self.take=self.getTake(layer)
    def getTake(self):
        fetch=self.layer.get("fetch")
        take={
            "key":fetch.get("key"),
            "type":self.outConfig.get("type") # 为的是以后扩展 , 解析take 可以写成一个类
        }
        take[self.outConfig.get("type")]=self.outConfig.get(self.outConfig.get("type"))
        return take 
    def getInfectHook(self,hook,infect ):
        for i in range(1,len(self.chains)):
                cursor=self.chains[i-1]
                next=self.chains[i]
                if getChildLevel(hook):
                    if cursor[hook]!=next[hook]:
                        infect=hook 
                        return 
                    else:
                        self.getInfectHook(getChildLevel(hook,infect ))
        return infect 
         

    def spread(self):
        RNA=self.take
        for r in self.chains:
            infect=self.getInfectHook(r.get("topHook")) or "cell"
            while getChildLevel(infect):
                r[infect].take = RNA
                infect=getChildLevel(infect)
        pass


class ContactVirus:

    def __init__(self, chain, nextChain, outConfig):
        self.chain= chain
        self.nextChain= nextChain
        self.outConfig = outConfig
        self.cellLayer=chain.getLayer("cell")
        self.take = self.getTake()

    def getTake(self):
        fetch = self.cellLayer.get("fetch")
        take = {
            "key": fetch.get("key"),
            "type": self.outConfig.get("type")  # 为的是以后扩展 , 解析take 可以写成一个类
        }
        take[self.outConfig.get("type")] = self.outConfig.get(self.outConfig.get("type"))
        return take

    def getInfectHook(self):

        cursor = self.chain
        next = self.nextChain
        infect=cursor.get("topHook")
        if next:
            while infect:
                layer_cursor = cursor.get(infect)
                layer_next = next.get(infect)
                if equalObj(layer_cursor.get("fetch").get("key"),layer_next.get("fetch").get("key")):
                    layer=cursor.getChildLayer(infect)
                    if layer:
                        infect= layer.get("hook")
                else:
                    infect=layer_cursor .get("hook")
                    break
        return infect

    def doLog(self,hook,data):
        pass
        print "haha~haha "



    def spread(self):
        RNA = self.take
        infect=self.getInfectHook()
        self.chain[infect].take=RNA
        self.doLog(infect,self.chain[infect])

        while getChildLevel(infect):
            infect=getChildLevel(infect)
            self.chain[infect].take = RNA
            self.doLog(infect,self.chain[infect])