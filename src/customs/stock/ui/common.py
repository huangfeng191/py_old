# -*- coding: utf-8 -*-
# Module  :
# Author  : fengfeng
# Date    : 2018-07-25
# Version : 1.0

from ui import path, wildcard, CRUD,web
from customs.stock.service.tushare_api import *
from service.biz import user,customer
import web
import json
from misc import utils

from web.contrib.template import render_mako
render_out = render_mako(directories=[ "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")


@path("/ctx.js")
class Ctx:


    def GET(self, _customer=None, _cid=None, _role=None, *args, **kwArgs):

        web.header("Content-Type", "text/javascript", True)
        # user=utils.get_session_value('user')
        u=user.get({"acc":"sandy"})
        c = customer.get({"code": "uniscada"})
        GCtx={}

        GCtx["user"]=u
        GCtx["customer"]=c
        return "var GCtx = %s; " % json.dumps(GCtx)




@path("/out/index.html")
class OutIndex:
    def GET(self, _cid = None, *args, **kwargs):
        return render_out["webpack/out"]()

