
# -*- coding: UTF-8 -*-
# Module  : py
# Description :获取数据
# Author  : Wujj
# Date    : 2019/08/11
# Version : 1.0

import ctx

from misc.inteface import *
from copy import deepcopy
import tushare_proapi as pro
import json
import time
#坐标
def getBaiduCoordinates():
    # ?query=浙江&output=json&ak=UFlVB3ZbqW14mWnengtXM0QbYVGHgM7U&region=302
    default={"query":"","output":"json","ak":ctx.baiduToken,"region":"302"}
    l=pro.stock_company.items(query={"position":{'$exists':0}})
    for r in l:
        office=r.get("office")
        if( len(office.split(","))>1):
            office=office.split(",")[0]
        query = dict(default, **deepcopy({"query":office}))
        ret=toGetUrl("http://api.map.baidu.com/place/v2/search",
        query)
        ret=json.loads(ret)
        if(ret.get("status")==0 and  len(ret.get("results"))):
            r["position"]=ret.get("results")[0].get("location")
            pro.stock_company.upsert(**r)
        time.sleep(1)
    return "OK"
