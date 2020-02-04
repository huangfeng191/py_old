# -*- coding: UTF-8 -*-
# Module  : py
# Description :分层数据处理
# Author  : Wujj
# Date    : 2020/1/31
# Version : 1.0

from  customs.tide.service.bean import base as base


class layer:
    def __init__(self,level ):
        self.module =base["tide_"+level]
        self.fetch={
            "key":["sn","cycle","level","t"],
            "option":["refresh"],
        }

    def getById(self,_id):

        return self.module.get(_id)
    def getOne(self,query={}):

        return self.module.one(query)
    def getFetch(self,_id="",query={}):
        layer=None
        fetch=None
        if _id:
            layer=self.getById(_id)
        else:
            layer=self.getOne(query)

        if layer:
           fetch={}
           for k in  self.fetch.keys():
                for s in self.fetch.get(k):
                    fetch[k][s]=layer.get(s)
        return fetch


def test_layer():
    print 1