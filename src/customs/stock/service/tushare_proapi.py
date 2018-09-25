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

# 考虑用on_upsert
#stock_basics.inject(industry_classified,"i_c","code",False,"code")

import json
import time

import tushare as ts


def getInterfaceData(tp="stock_basic",fields=None,**kwargs):
    pro = ts.pro_api(token="ec3db7ff2556c111a95e7b89af5ba650a3064eb6f71c3b48eebc151c")
    data=pro.query('stock_basic',fields,**kwargs )
    return data

def getProInfo(table_nm,method=None,icount=1):
    fields=[]
    if table_nm:
        configRow=pro_interface_config.get({"table_nm":table_nm})
        for r in configRow.get("colInp").split("\n"):
            ar = r.split(",")
            if ar[0]:
                fields.append(ar[0])
    if method:
        df=getInterfaceData(tp=method,fields=fields)
    else:
        df= getInterfaceData(tp=table_nm,fields=fields)

    if configRow:
        indexKey=  configRow.get("indexKey")
    df_index=df.index
    if not isinstance(df,list):
        print "OK"
        l=json.loads(df.to_json(orient='records'))
        for i,r in enumerate(l):
            if indexKey:
               r[indexKey]=df_index[i]
            eval(table_nm).upsert(**r)
    else:
    #     考虑写入错误日志 ，重新发起请求
        time.sleep(10)
        print "err"
        if icount<5:
            getProInfo(table_nm,method,icount=icount+1)
        else:
            print "total_err"
    return "OK"
