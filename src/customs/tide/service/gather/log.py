# -*- coding: UTF-8 -*-
# Module  : py
# Description :cell step 等的 log
# Author  : Wujj
# Date    : 2020/2/29
# Version : 1.0

from customs.tide.service.gather.layer import *
from  customs.tide.service import utils as tide_utils
# from customs.tide.service.persistence.method import *
from customs.tide.service.persistence import *




class CellLog:
    def __init__(self,fetch=None,layer=None,isNew=False):
        self.module=tide_cell_log
        if isNew:
            self.layer=layer
            pass
        else:
            self.bindLayer(fetch)
    def bindLayer(self,fetch):
        self.layerLog=LayerLog("cell",fetch.get("key"))
        self.layer=self.layerLog.get()

    def save(self):
        layer=self.layer
        if "basket" in layer:
            del layer["basket"]
        self.module.upsert(**layer)
        self.bindLayer(layer.get("fetch"))


    def getLayerLog(self):
        return self.layerLog
    def getLayer(self):
        return self.layer
    def getData(self):
        take = self.layer.get("take")
        emphasis=EmphasisTake(take)
        ret=emphasis.get()
        return ret
        pass

