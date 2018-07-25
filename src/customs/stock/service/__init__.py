# -*- coding: UTF-8 -*-
# Description :
# Author  : fengfeng
# Date    : 2017/07/16
# Version : 1.0


import ctx
from service import comm
stock_store = comm.CRUD(ctx.cmdb, "stock_store", [("cid", 1)])
stock_adminsave = comm.CRUD(ctx.stockdb, "adminsave", [("cid", 1)])
stock_interface_config = comm.CRUD(ctx.stockdb, "interface_config" )
stock_test = comm.CRUD(ctx.stockdb, "test", [("cid", 1)])
import tushareapi