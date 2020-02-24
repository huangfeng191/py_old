# -*- coding: UTF-8 -*-
# Module  : py
# Description : 将 rule 后的对象 扩散开来
# Author  : Wujj
# Date    : 2020/2/16
# Version : 1.0

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
        take[self.outConfig.get("type")]=outConfig.get(self.outConfig.get("type"))
        return take 
    def getInfectHook(self,hook):
        for i in range(1,len(self.chains)):
                cursor=self.chains[i-1]
                next=self.chains[i]
                if getChildLevel(hook):
                    if cursor[hook]!=next[hook]:
                        infect=hook 
                        return 
                    else:
                        getInfectHook(getChildLevel(hook))  
        return infect 
         

    def spread(self):
        RNA=self.take
        for r in self.chains:
            infect=self.getInfectHook(r.get("topHook")) or "cell"
            
