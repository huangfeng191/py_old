# -*- coding: UTF-8 -*-
# Module  : py
# Description :基本接口
# Author  : Wujj
# Date    : 2017-11-5
# Version : 1.0



import ctx
from service import comm
stock_basics = comm.CRUD(ctx.tusharedb, "stock_basics", [("cid", 1)])

import json
import time

import tushare as ts


def get_stock_basics():
    t=time.time()
    df=ts.get_stock_basics()
    l=json.loads(df.to_json(orient='records'))
    for r in l:
        stock_basics.upsert(**r)
    print time.time()-t
    return "OK"