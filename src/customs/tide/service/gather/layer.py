# -*- coding: UTF-8 -*-
# Module  : py
# Description :分层数据处理
# Author  : Wujj
# Date    : 2020/1/31
# Version : 1.0

from  customs.tide.service.bean import base as base

import json

# need to finish
def compressObject(obj):
    def plusKey(base,key,val,compressed):
        if type(val)== dict:
            for k, v in val.items():
                if type(v) == dict:
                    base = k + "."

                    plusKey()
        else:
             compressed[base+key]=val

    o={}
    base = ""
    compressed={}
    for k,v in obj.items():
        plusKey(base,k,v,compressed)

    return o

class LayerLog:

    def __init__(self,hook,fetchKey):
        self.hook=hook
        self.log=eval(("base.tide_%s_log") % hook).get(fetchKey)
        self.take=self.log.get("take") if self.log else None
        self.fetch=self.log.get("fetch") if self.log else None
        if not self.take:
            raise Exception("未找到layer 的 历史记录,请先生成 %s"% json.dumps(self.fetch))
    def getTake(self):
        return self.take;