# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/2/12
# Version : 1.0



from method import *

from tache import *

class CellDoing:
    def __init__(self,cell_layer,chain):
        self.cell_layer=cell_layer
        self.basket=cell_layer.getBasket()
        self.chain=chain


    def go(self):
        basket=self.basket
        d_layer=self.cell_layer.getLayer()
        S=CellSourceConfig(basket.get("sourceType"),
                           basket.get("sourceConfig"),d_layer)
        source=S.get()
        R =CellRuleConfig(basket.get("ruleType"),
                             basket.get("ruleConfig"),d_layer)
        rule=R.get()

        if basket.get("ruleType")=="table":
            if source.get("type")=="table":
                l=rule_doing_table(source.get(source.get("type")),rule)
        pass

#     完善 chain.cell 对象
# source
# loop
# rule
# out
