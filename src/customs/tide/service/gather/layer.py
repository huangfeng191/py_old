# -*- coding: UTF-8 -*-
# Module  : py
# Description :分层数据处理
# Author  : Wujj
# Date    : 2020/1/31
# Version : 1.0

from  customs.tide.service.bean import base as base

from  customs.tide.service import utils as tide_utils

import json




class LayerLog:

    def __init__(self,hook,fetchKey={},id=None):
        self.hook=hook
        compressedKey=tide_utils.compressObject({"fetch.key":fetchKey})
        if id:
            compressedKey=id
        self.log=eval(("base.tide_%s_log") % hook).get(compressedKey)
        self.take=self.log.get("take") if self.log else None
        self.fetch=self.log.get("fetch") if self.log else None
        if not self.fetch:
            raise Exception("未找到layer 的 历史记录,请先生成 fetch.key: %s"% json.dumps(fetchKey))
    def getTake(self):
        return self.take;
    def get(self):
        return self.log;

class Layer:
    def __init__(self,layer):
        self.layer=layer
        self.hook=layer.get("hook")

        self.basket = self.parseBasket()
        self.layer["basket"]=self.basket


    def parseBasket(self):
        basket={}
        try:
            config= self.layer.get("config") or{}
            if self.hook=="cell":
                for s in ["loopType","sourceType","ruleType","outType"]:
                    basket[s]= config.get(s)
                for s in ["loopConfig","sourceConfig","ruleConfig","outConfig"]:
                    if config.get(s):
                         basket[s] =json.loads( config.get(s))
                    else:
                        basket[s]={}
                for s in ["subjoin"]:
                    if config.get(s):
                        basket[s]=config.get(s,"").split("\n")
        except:
            print "解析参数错误"
            raise Exception("解析参数错误 gather.Layer.parseBasket")
        return basket

    def getBasket(self):
        return self.basket
    def getLayer(self):
        return self.layer

