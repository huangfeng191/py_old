# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/1/31
# Version : 1.0


from ui import path
import web
import json

from service.biz import  ddics

@path("/tide/bindings.js")
class StockBindings:


    def GET(self, _customer=None, _cid=None, _role=None, *args, **kwArgs):
      web.header("Content-Type", "text/javascript", True)
      bindings= []

      for dd in ddics.items(size=99999):
              bindings.append(dd)

      return "var GBindings = %s; " % json.dumps(bindings)
