# -*- coding: utf-8 -*-
# Module  :
# Author  : fengfeng
# Date    : 2017-07-16
# Version : 1.0

from ui import path, wildcard, CRUD
from customs.stock.service import *
# import tushare as ts
import json
import ctx

####################### in use
import service.comm as comm
import second
import common
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


##############################in use
@path("/stock/test.html")
class StockTest:
    def GET(self, _cid=None, *args, **kwargs):
        # return render_stock["test"]()
        return "ok111"


@wildcard("/stock/test/")
class StockTestCRUD(CRUD):
    def __init__(self):
        self.module = stock_test

    def queryByParent(self, pid):
        return list(comm.memus.items(query={"pid": pid}))

    def set_subMenus(self,id, menus):
        """
    根据传递过来的父菜单id，递归设置各层次父菜单的子菜单列表
    
    :param id: 父级id
    :param menus: 子菜单列表
    :return: 如果这个菜单没有子菜单，返回None;如果有子菜单，返回子菜单列表
    """
        # 记录子菜单列表
        subMenus = []
        # 遍历子菜单
        for m in menus:
            if m.parent == id:
                subMenus.append(m)

                # 把子菜单的子菜单再循环一遍
        for sub in subMenus:
            menus2 = self.queryByParent(sub.id)
            # 还有子菜单
        if len(menus):
            sub.subMenus = self.set_subMenus(sub.id, menus2)

            # 子菜单列表不为空
        if len(subMenus):
            return subMenus
        else:  # 没有子菜单了
            return None

    def query(self, count=True, *args, **kwArgs):

        return "ok"
