# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/3/2
# Version : 1.0


from method import *
from  customs.tide.service import utils as tide_utils
from customs.tide.service.bean.base import *
class EmphasisTake:
    '''
        take
            type
            config
    '''
    def __init__(self,take):
        self.take=take
        self.type=take.get("type")

    def get(self):
        config=self.take.get(self.type)
        take=self.take
        ret=None
        if self.type=="table":
            data=rule_doing_table(config,None)
            if config.get("fields"):
                pass
                # config=config.get("fields")
        elif self.type=="log":
            bean=eval("tide_%s_log"%config.get("hook"))
            fetchKey=tide_utils.compressObject({"fetch.key":take.get("key")})
            o=bean.get(fetchKey)
            if o.get("data"):
                ret ={}
                for s in config.get("fields"):
                    ret[s]=o["data"].get(s)
        return ret


def doTideLog(hook, data):
    if hook != "cell":

        fetchKey = tide_utils.compressObject({"fetch.key": data.get("fetch").get("key")})
        bean=eval("tide_%s_log" % hook)
        old=bean.get(fetchKey)
        if old:
            old.update(data)
            data=old
        eval("tide_%s_log" % hook).upsert(**data)
