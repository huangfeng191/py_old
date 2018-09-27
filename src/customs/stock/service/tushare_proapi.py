# -*- coding: UTF-8 -*-
# Module  : py
# Description :基本接口
# Author  : Wujj
# Date    : 2017-11-5
# Version : 1.0



import ctx
from service import comm
pro_admin_save = comm.CRUD(ctx.tuprodb, "admin_save", [("cid", 1)])
pro_interface_config = comm.CRUD(ctx.tuprodb, "interface_config" )

# 获取股票基本信息
stock_basic = comm.CRUD(ctx.tuprodb, "stock_basic", [("code", 1)])
# 沪深股通成份股
hs_const = comm.CRUD(ctx.tuprodb, "hs_const", [("code", 1)])

# 考虑用on_upsert
#stock_basics.inject(industry_classified,"i_c","code",False,"code")

import json
import time

import tushare as ts

# table_nm 就是接口名
def getInterfaceData(table_nm="stock_basic",fields=None,**kwargs):
    pro = ts.pro_api(token="ec3db7ff2556c111a95e7b89af5ba650a3064eb6f71c3b48eebc151c")
    data=pro.query(table_nm,fields,**kwargs )
    return data

def handleDate(table_nm,fields,config,**kws):

    df = getInterfaceData(table_nm=table_nm, fields=fields, **kws)
    # df_index = df.index
    # 暂时不用
    if not isinstance(df, list):
        print "OK"
        l = json.loads(df.to_json(orient='records'))
        for i, r in enumerate(l):
            eval(table_nm).upsert(**r)


def getProInfo(table_nm,icount=1,**kwargs):

    if table_nm:
        configRow=pro_interface_config.get({"table_nm":table_nm})
        fields = []
        for r in configRow.get("colInp").split("\n"):
            ar = r.split(",")
            if ar[0]:
                fields.append(ar[0])

        if configRow.get("param"):
            params=json.loads(configRow.get("param"))
            for r in params:
                handleDate(table_nm,fields,configRow,**r)
        else:    
            handleDate(table_nm,fields,configRow)


    return "OK"
