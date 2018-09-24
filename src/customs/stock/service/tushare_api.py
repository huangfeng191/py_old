# -*- coding: UTF-8 -*-
# Module  : py
# Description :基本接口
# Author  : Wujj
# Date    : 2017-11-5
# Version : 1.0



import ctx
from service import comm
stock_admin_save = comm.CRUD(ctx.tusharedb, "stock_admin_save", [("cid", 1)])
stock_interface_config = comm.CRUD(ctx.tusharedb, "stock_interface_config" )
# 获取股票基本信息
stock_basics = comm.CRUD(ctx.tusharedb, "stock_basics", [("code", 1)])
# 行业分类
industry_classified = comm.CRUD(ctx.tusharedb, "industry_classified", [("code", 1)])
# 概念分类
concept_classified = comm.CRUD(ctx.tusharedb, "concept_classified", [("code", 1)])

# 地域分类
area_classified = comm.CRUD(ctx.tusharedb, "area_classified", [("code", 1)])

# 考虑用on_upsert
#stock_basics.inject(industry_classified,"i_c","code",False,"code")

import json
import time

import tushare as ts

def getInfo(table_nm,method=None,icount=1):
    if table_nm:
        configRow=stock_interface_config.get({"table_nm":table_nm})
    if method:
        df=eval("ts.%s"%method)()
    else:
        df=eval("ts.get_%s"%table_nm)()
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
            getInfo(table_nm,method,icount=icount+1)
        else:
            print "total_err"
    return "OK"
