# -*- coding: UTF-8 -*-
# Module  : py
# Description :获取数据
# Author  : Wujj
# Date    : 2017-11-4
# Version : 1.0


from ui import path, CRUD, wildcard
from web.contrib.template import render_mako
from customs.stock.service import *
import customs.stock.service.tushare_proapi  as tushare_proapi
render_prostock = render_mako(directories=["customs/stock/templates/pro", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")




@path("/prostock/admin.html")
class StockAdmin:
    def GET(self, _cid=None, *args, **kwargs):
        return render_prostock["admin"]()


@wildcard("/prostock/admin/")
class StockAdminCRUD(CRUD):
    def __init__(self):
        self.module = tushare_proapi.stock_admin_save
    def action(self, act, *args, **kwArgs):
        if act == 'basics':
            return self.basics(*args, **kwArgs)
        return CRUD.action(self, act, *args, **kwArgs)
    def getProInfo(self, table_nm=None, *args, **kwArgs):
        tushare_proapi.getProInfo(table_nm)
        print 1
        return "OK"
