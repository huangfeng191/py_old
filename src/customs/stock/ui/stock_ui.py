# -*- coding: UTF-8 -*-
# Description 查询数据
from ui import path, CRUD, wildcard
from web.contrib.template import render_mako
from customs.stock.service.tushare_api import *
render_stock = render_mako(directories=["customs/stock/templates", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")

from customs.stock.ui import bindinterfaceConfig


@path("/stock/interfaceconfig.html")
class StockInterfaceconfig:
    def GET(self, _cid=None, *args, **kwargs):
        return render_stock["interfaceconfig"]()


@wildcard("/stock/interfaceconfig/")
class StockInterfaceconfigCRUD(CRUD):
    def __init__(self):
        self.module = stock_interface_config
    def query(self, count=True, *args, **kwArgs):

       res = CRUD.query(self, count=count, *args, **kwArgs)

       return res



@path("/stock/interfacedata.html")
class StockInterfaceData:
    def GET(self, _cid = None, *args, **kwargs):
        return render_stock["interfaceData"]()


@wildcard("/stock/interfacedata/")
class StockInterfaceDataCRUD(CRUD):

    def __init__(self):
        self.module = stock_interface_config
    @bindinterfaceConfig
    def action(self, act, *args, **kwArgs):
         return CRUD.action(self, act, *args, **kwArgs)



