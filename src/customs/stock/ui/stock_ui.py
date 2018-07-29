# -*- coding: UTF-8 -*-
# Description 查询数据
from ui import path, CRUD, wildcard
from web.contrib.template import render_mako
from customs.stock.service import *
render_stock = render_mako(directories=["customs/stock/templates", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")




@path("/stock/interfaceconfig.html")
class StockInterfaceconfig:
    def GET(self, _cid=None, *args, **kwargs):
        return render_stock["interfaceconfig"]()


@wildcard("/stock/interfaceconfig/")
class StockInterfaceconfigCRUD(CRUD):
    def __init__(self):
        self.module = stock_interface_config