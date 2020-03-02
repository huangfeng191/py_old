# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/2/12
# Version : 1.0


from tache import *

from customs.tide.service.gather.log import *

class CellDoing:
    def __init__(self,cell_layer,chain):
        self.cell_layer=cell_layer
        self.layer=cell_layer.getLayer()
        self.basket=cell_layer.getBasket()
        self.chain=chain

    def method(self,basket,source,rule):
        data=None
        if basket.get("ruleType")=="table":
            if source.get("type")=="table":
                data=rule_doing_table(source.get("table"),rule)
        return data

    def go(self):
        basket=self.basket
        d_layer=self.cell_layer.getLayer()
        S = CellLoopConfig(d_layer)
        loop = S.get()
        pass
        S=CellSourceConfig(d_layer)
        source=S.get()
        R =CellRuleConfig(basket.get("ruleType"),
                             basket.get("ruleConfig"),d_layer)
        rule=R.get()

        data=self.method(basket,source,rule)
        O=CellOutConfig(basket.get("outType"),basket.get("outConfig"),d_layer)
        data=O.go(data)
        pass
        cellLog=CellLog(**{"layer":d_layer,"isNew":True})
        cellLog.accrue(data)
        pass

    def getLayer(self):
        return self.layer


