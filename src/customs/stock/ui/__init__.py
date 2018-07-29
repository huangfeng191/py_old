# -*- coding: utf-8 -*-
# Module  :
# Author  : fengfeng
# Date    : 2017-07-16
# Version : 1.0
import web
from customs.stock.service.tushare_api import *

def bindinterfaceConfig(func):
    def _bindinterfaceConfig(self,act, *args, **kwArgs):
        params = web.input(table_nm='')
        if( act in ["query","insert","update","delete","importData"]) and params.get("table_nm"):
          # self.module=eval(params.get("table_nm"))
          self.module=eval(params.get("table_nm"))
          return func(self,act, *args, **kwArgs)
        return func(self,act, *args, **kwArgs)
    return _bindinterfaceConfig


import common
import stock_ui
import stock_api


