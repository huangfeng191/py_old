# -*- coding: utf-8 -*-
# Module  :
# Author  : fengfeng
# Date    : 2017-07-16
# Version : 1.0

from ui import path, wildcard, CRUD
from customs.stock.service import stock_store
import tushare as ts
import json
import ctx


# 设备管理
@path("/stock/equipmanage.html")
class StockEquipManage:
    def GET(self, _cid=None, *args, **kwargs):
        return "wonderful"


@wildcard("/stock/division/")
class StockDivisionCRUD(CRUD):
    def __init__(self):

        self.module = stock_store

    def action(self, act, *args, **kwArgs):
        if act == 'aduit':
            return self.aduit(*args, **kwArgs)
        else:
            return CRUD.action(self, act, *args, **kwArgs)

    def insert(self, record=None, *args, **kwArgs):
        print 1
        # if not record:
        #     from customs.stock.service.dataapi import Client
        #     try:
        #         client = Client()
        #         client.init('13d3ae777dfca314b3cfcabe0b6ae7c228e793dfd347ea41b2aba63660c2f1ff')
        #         url1 = '/api/equity/getEqu.json?field=&listStatusCD=&secID=&ticker=&equTypeCD=A'
        #         code, result = client.getData(url1)
        #         if code == 200:
        #             print result
        #         else:
        #             print code
        #             print result
        #
        #     except Exception, e:
        #         # traceback.print_exc()
        #         raise e
        #
        #     return self.module.insert(json.loads(result.to_json(orient='data')))

    def aduit(self):

        return "ok111"
