# -*- coding: UTF-8 -*-
# Module  : py
# Description :基本接口
# Author  : Wujj
# Date    : 2017-11-5
# Version : 1.0



import ctx
from copy import deepcopy
from service import comm
pro_admin_save = comm.CRUD(ctx.tuprodb, "admin_save", [("cid", 1)])
pro_interface_config = comm.CRUD(ctx.tuprodb, "interface_config" )
pro_multi_data = comm.CRUD(ctx.tuprodb, "multi_data" )

# 获取股票基本信息
stock_basic = comm.CRUD(ctx.tuprodb, "stock_basic", [("ts_code", 1)])
# 沪深股通成份股
hs_const = comm.CRUD(ctx.tuprodb, "hs_const", [("ts_code", 1)])
# 股票曾用名
namechange = comm.CRUD(ctx.tuprodb, "namechange", [("ts_code", 1)])

# 考虑用on_upsert
#stock_basics.inject(industry_classified,"i_c","code",False,"code")

import json
import time
from misc import utils
import tushare as ts

# table_nm 就是接口名
def getInterfaceData(table_nm="stock_basic",fields=None,**kwargs):
    pro = ts.pro_api(token="ec3db7ff2556c111a95e7b89af5ba650a3064eb6f71c3b48eebc151c")
    data=pro.query(table_nm,fields,**kwargs )
    return data
# 将数据保存到数据库
def handleDate(table_nm,fields,config,**kws):

    df = getInterfaceData(table_nm=table_nm, fields=fields, **kws)
    # df_index = df.index
    # 暂时不用
    key_query={}
    key_last=""
    if config.get("indexKey"):
        for r in config.get("indexKey").split(","):
            key_query[r]=None
            key_last=r

    if not isinstance(df, list):
        print "OK"
        l = json.loads(df.to_json(orient='records'))
        for i, r in enumerate(l):
            # 从对象中获取primary
            k_query= dict(filter(lambda o: o[0] in key_query.keys(), r.items()))
            r_one=eval(table_nm).get(k_query)
            if r_one:
                r=dict(r_one,**deepcopy(r))
            eval(table_nm).upsert(**r)
            # ---------------------------------------------
            # 数组对象插入配置
            if("2" in config.get("storage_way",[]) or[] ):
                # 支持插入多个表
                for storage_config in config.get("storage_config","").split("\n"):
                    if storage_config.split(",")>1:
                        storage_table_nm=storage_config.split(",")[0]
                        storage_table_psn=storage_config.split(",")[1]
                        InjectArray(r,storage_table_nm,{storage_table_psn:r.get(storage_table_psn)},k_query,key_last,config)
def InjectArray(r,storage_table_nm=None,storage_table_psn={},query={},sort="",config={},**kwargs):
    table_nm=config.get("table_nm")
    one=eval(storage_table_nm).get(storage_table_psn)
    if one:
        if not one.get(table_nm,[]):
            one[table_nm]=[]
        target_arr=one.get(table_nm,[])
        isNew=True
        for one_r in target_arr:
            if utils.dict_compare(one_r,query):
                one_r.update(r)
                isNew=False
        if isNew:
            target_arr.append(r)        
        if sort:
            target_arr.sort(key=lambda x:x.get(sort))
            one[table_nm+"2o"]=target_arr[-1]
        eval(storage_table_nm).upsert(**one)
    else:
        pass



def getProInfo(table_nm,icount=1,**kwargs):

    if table_nm:
        configRow=pro_interface_config.get({"table_nm":table_nm})
        fields = []
        for r in configRow.get("colInp").split("\n"):
            ar = r.split(",")
            if ar[0]:
                fields.append(ar[0])
        # 方法参数  目的是接口可能有参数要求，写成了一个数组，可循环调用接口
        if configRow.get("param"):
            params=json.loads(configRow.get("param"))
            for r in params:
                handleDate(table_nm,fields,configRow,**r)
        else:    
            handleDate(table_nm,fields,configRow)


    return "OK"
