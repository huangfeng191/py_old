# -*- coding: UTF-8 -*-
# Description :
# Author  : fengfeng
# Date    : 2017/07/16
# Version : 1.0


import ctx
from service import comm
stock_store = comm.CRUD(ctx.cmdb, "stock_store", [("cid", 1)])