# -*- coding: UTF-8 -*-
# Module  : py
# Description :第二次尝试
# Author  : Wujj
# Date    : 2017-11-4
# Version : 1.0

from bson import ObjectId
from ui import path, CRUD, wildcard
from web.contrib.template import render_mako
from customs.stock.service import *
import customs.stock.service.tushareapi  as tushareapi
render_n = render_mako(directories=["customs/stock/templates", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")
@path("/stock/admin.html")
class StockAdmin:
    def GET(self, _cid=None, *args, **kwargs):
        return render_n["admin"]()


@wildcard("/stock/admin/")
class StockAdminCRUD(CRUD):
    def __init__(self):
        self.module = stock_adminsave
    def action(self, act, *args, **kwArgs):
        if act == 'basics':
            return self.basics(*args, **kwArgs)
        else:
            return CRUD.action(self, act, *args, **kwArgs)

    def basics(self, record=None, *args, **kwArgs):
        tushareapi.get_stock_basics()
        print 1
