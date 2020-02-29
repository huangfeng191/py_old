# -*- coding: UTF-8 -*-
# Module  : py
# Description :cell step 等的 log
# Author  : Wujj
# Date    : 2020/2/29
# Version : 1.0

from customs.tide.service.bean.base import *
from customs.tide.service.gather.layer import *
from  customs.tide.service import utils as tide_utils

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
    def infoResolve(self,fetch,info):
        refresh = fetch.get("option").get("refresh")
        config=info.get(info.get("type"))
        if refresh=="refresh":
            if info.get("type")=="table":
                id=tide_utils.compressObject(config.get("query",{}))
                eval(config.get("nm")).delete(id, multi=True)
        pass
    def dataResolve(self,fetch,info,take,data):
        layer=self.layer
        compressedKey = tide_utils.compressObject({"fetch.key": fetch.get("key")})
        old = self.module.get(compressedKey)
        if old:
            pass
        else:
            config = info.get(info.get("type"))
            if take.get("type")=="log":
                for s in config.get("fields",[]):
                    if "data" not in layer:
                        layer["data"]={}
                    layer["data"][s]=data.get(s)
            elif take.get("type")=="table":
                if type(data)==dict :
                    data=[data]
                for r in data:
                    r.update(info.get("query"))
                    eval(config.get("nm")).upsert(**r)
            self.module.upsert(**layer)
            self.bindLayer(fetch)

    def accrue(self,data):
        fetch=self.layer.get("fetch")
        info=self.layer.get("info")
        take=self.layer.get("take")
        self.infoResolve(fetch,info) # 处理历史记录
        self.dataResolve(fetch,info,take,data) # 处理数据

    def getLayerLog(self):
        return self.layerLog
    def getLayer(self):
        return self.layer
    def getData(self):
        pass
