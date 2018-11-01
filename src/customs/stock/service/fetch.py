# -*- coding: UTF-8 -*-
# Module  : py
# Description :获取数据
# Author  : Wujj
# Date    : 2018/10/31
# Version : 1.0


from customs.stock.service.tushare_proapi import *

from customs.stock.service import basic


# table_nms [] 返回表的字段信息
def bindExplain(table_nms=[]):
    explain = {}
    #     获取字段注释
    for s in table_nms:
        one_config = basic.pro_interface_config.get({"table_nm": s})
        one_o = basic.config_col_obj(one_config)
        if one_o and one_o.get("a"):
            explain[s] = one_o
    return explain


# codes:[{"code":1,basic:"",self_query:{}}]
# items:{"daily":{"basic":"stock_basic"}}

# 将查询的对象归类
# table_nms ["daily"....]
# 可以考虑拼装出统一的返回结果
# ret :
# explain: 注释
# table_nms:[] 查询对象
# stock_basic:{}...
def bindTables(table_nms=[]):
    basic_table_o = {
        "stock_basic": {
            "daily": {"k": "ts_code", "crux": {"trade_date": "交易日期", "close": "收盘价"}, "desc": ""},
            "daily_basic": {"k": "ts_code",
                            "crux": {"trade_date": "交易日期", "turnover_rate": "换手率", "turnover_rate": "换手率（自由流通股）",
                                     "pe": "市盈率（总市值/净利润）"}, "desc": ""},
        },
        "index_basic": {
            "index_daily": {"k": "ts_code", "crux": {"trade_date": "交易日期", "pct_change": "涨跌幅", "close": "收盘点位"},
                            "desc": ""}
        }
    }
    o_simple = {}
    # 查找对象的上级对象
    for k, v in basic_table_o.items():
        for k2, v2 in v.items():
            o_simple[k2] = k

    retO = {"table_nms": table_nms, "explain": {}}
    for s in table_nms:
        if o_simple.get(s) not in retO:
            retO[o_simple.get(s)] = {}
        retO[o_simple.get(s)][s] = basic_table_o.get(o_simple.get(s)).get(s)
    # 注释
    retO["explain"] = bindExplain(table_nms=table_nms)
    return retO


def bindData(
        # 此处为bindTables 返回对象
        stock_basic=None, index_basic=None, table_nms=None, explain=None,
        # 查询时间
        time_q={},
        # { "index_daily": {"k": "000008.SH","query":{}}}
        table_q={},
        reverse=False,
        **kwargs):

    reverse= -1 if reverse else 1

    ret = {}
    if table_nms:
        ret["table_nms"] = table_nms
    if explain:
        ret["explain"] = explain


    for s in ["stock_basic","index_basic"]:
        if eval(s):
            ret[s]=eval(s)
            for k, v in eval(s).items():
                table_one=table_q.get(k) or {}# {query:{},k:""...}
                # 对k 数据查询
                table_k=v.get("k") # 配置表中的主键
                table_q={}
                if table_k and table_one.get("k"):
                    table_q[table_k]=table_one.get("k")
                table_q.update(time_q)
                table_q.update(table_one.get("query",{}))
                ret[s]["a"]=list(eval(k).items(query=table_q, _sort=[("ts_code", reverse)]))
                pass
    return ret

def getDatas(table_q,table_nms=[], time_q={},reverse=True):
    comm_o=bindTables(table_nms)
    comm_o["table_q"]=table_q
    comm_o["time_q"] = time_q
    ret=bindData(**comm_o)
    return ret



def bindDatas1(items={}, oBasic=None, time_q={}, reverse=False, **kwArgs):
    if reverse:
        reverse = -1
    else:
        reverse = 1

    record = {}
    if oBasic:
        record["code"] = oBasic.get("ts_code")
        record["o_basic"] = oBasic
    explain = {}
    if not items:
        items = {
            "daily": {},
            "daily_basic": {},

            "index_daily": {"ts_code": "000008.SH"}
        }
    # 获取字段注释
    for s in items.keys():
        one_config = basic.pro_interface_config.get({"table_nm": s})
        one_o = basic.config_col_obj(one_config)
        if one_o and one_o.get("a"):
            explain[s] = one_o

    if "daily" in items:
        l = daily.items(query=dict({"ts_code": oBasic.get("ts_code")}, **time_q), _sort=[("ts_code", reverse)])
        record["daily"] = list(l)

    if "daily_basic" in items:
        l = daily_basic.items(query=dict({"ts_code": oBasic.get("ts_code")}, **time_q),
                              _sort=[("ts_code", reverse)])
        record["daily_basic"] = list(l)

    if "index_daily" in items:
        l = index_daily.items(query=dict({"ts_code": items.get("index_daily").get("ts_code")}, **time_q),
                              _sort=[("ts_code", reverse)])
        record["index_daily"] = list(l)
    return record, explain
