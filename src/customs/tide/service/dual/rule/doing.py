# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/2/12
# Version : 1.0


from tache import *

from customs.tide.service.utils.wrap import *
from customs.tide.service.gather.log import *
from customs.tide.service.persistence.pd import *

class CellDoing:
    def __init__(self,cell_layer,chain,chains=None):
        self.cell_layer=cell_layer
        self.layer=cell_layer.getLayer()
        self.basket=cell_layer.getBasket()
        self.chain=chain
        self.chains=chains
    #  调用实际的方法
    def method(self,basket,source,carousel,rule):
        data=None
        if basket.get("ruleType")=="table":
            if source.get("type")=="table":
                if carousel:
                    if "query" not in rule:
                        rule["query"]={}
                    rule["query"].update(carousel)
                data=rule_doing_table(source.get("table"),rule)
        elif basket.get("ruleType")=="aggregate":
            if source.get("type") == "table":
                if carousel:
                    if "query" not in source["table"]:
                        source["table"]["query"] = {}
                    source["table"]["query"].update(carousel)

                data = rule_doing_aggregate(source.get("table"), rule)
        elif basket.get("ruleType") =="pandas":
            if source.get("type")=="table":
                if carousel:
                    if "query" not in rule:
                        rule["query"]={}
                    rule["query"].update(carousel)
                data=rule_doing_table(source.get("table"),rule)
            P=PandasDo(carousel,rule,data)
            data=P.go()
            pass
        return data



    def oldResolve(self,fetch,take):
        config=take.get(take.get("type"))
        if take.get("type")=="table":
            deleteTideLog("cell", fetch.get("key", {}))
            deleteTideTable(config.get("nm"),take.get("key"))
        elif take.get("type")=="log":
            deleteTideLog(config.get("hook"),fetch.get("key", {}))
        pass

    @runtime_times_wrapper("cell.carousel ",1000)
    def newResolve(self,basket, source,carousel, rule,Out,**kwargs):
        '''
            1. 获取规则数据
            2. 保存数据
        Args:
            basket:
            source:
            carousel:
            rule:
            Out:
            **kwargs:

        Returns:

        '''
        fetch = self.layer.get("fetch")
        take = self.layer.get("take")
        data = self.method(basket, source, carousel, rule)
        data = Out.go(data)  # 根据输出 处理数据
        self.dealData(fetch, take, carousel, data)  # 保存数据

    def dealData(self,fetch,take,carousel,data):
        '''
        生成数据
        Args:
            fetch:
            take:
            carousel: loop.one
            data:

        Returns:

        '''
        layer=self.layer
        config = take.get(take.get("type"))
        if take.get("type")=="log":
            if not data:
                data={}
            for s in config.get("fields",[]):
                if "data" not in layer:
                    layer["data"]={}
                layer["data"][s]=data.get(s)
        elif take.get("type")=="table":
            if not data:
                return
            if type(data)==dict :
                data=[data]
            for r in data:

                saveTideTable(config.get("nm"), take.get("key"),r,carousel)


    @runtime_wrapper("one cell execate")
    @runtime_times_wrapper_reset
    def go(self,**kwargs):
        pass
        fetch=self.layer.get("fetch")
        refresh=fetch.get("option").get("refresh")
        if refresh=="keep":
            pass
        else:
            self.accrue(**kwargs)

    # 生成数据

    def accrue(self,**kwargs):

        basket=self.basket
        d_layer=self.cell_layer.getLayer()
        loop_data=[None]
        refer=[]
        if basket.get("loopType"):
            L = CellLoopConfig(d_layer,self.chains)
            loop_data= L.getData()
            refer = L.getLoop().get("fields")
        S = CellSourceConfig(d_layer,self.chains)
        source = S.get()

        R = CellRuleConfig(basket.get("ruleType"),
                           basket.get("ruleConfig"), d_layer)
        rule = R.get()
        Out = CellOutConfig(basket.get("outType"), basket.get("outConfig"), d_layer)

        fetch = self.layer.get("fetch")
        take = self.layer.get("take")


        self.oldResolve(fetch,take )

        # 获取数据

        for r in loop_data:
            carousel={}
            for field in refer:
                carousel[field]=r.get(field)
            self.newResolve(basket, source, carousel, rule, Out,**kwargs)
            
        cellLog = CellLog(**{"layer": d_layer, "isNew": True})
        cellLog.save()

        # 记录日志



    def getLayer(self):
        return self.layer


