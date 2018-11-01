# -*- coding: UTF-8 -*-
# Description : proapi 报表
# Author  : fengfeng
# Date    : 2018/10/24
# Version : 1.0



from customs.stock.service.tushare_proapi import *
from customs.stock.service.fetch import *

from customs.stock.service import basic

# 已时间为记录
def rowToO(table_name,x_axis=[],y_axis=[],query=None):
    
    rows=eval(table_name).items(query=query,fields=set(x_axis+y_axis))

    
    pass

# 一般来说 x 指标是统一的
# y_axis 定义为数组对象
def rowToSimpleCharts(o_data,explain,in_xAxis={"k":"字段","from":"哪个表里的字段"},in_yAxis={},
                in_series=[{"k":"","from":"","yAxisIndex":""}],**kwArgs):

    # x轴
    xAxis={"type":"category","data":[],"name":"默认名字"}

    # 形成 {k:[]} 格式拼data  数据
    o_froms = {}

    if "from" in in_xAxis and "k" in in_xAxis:
        xAxis["name"]= explain[in_xAxis.get("from")]["o"].get(in_xAxis.get("k")).get("nm")
        if in_xAxis.get("from") not in o_froms:
            o_froms[in_xAxis.get("from")] = [in_xAxis.get("k")]
    xAxis.update(in_xAxis)
    # y轴
    yAxis=[{"type":"value"}]

    if in_yAxis:
        for n in in_yAxis.keys():
            if len(yAxis)<int(n)+1:
                yAxis=yAxis+[{"type":"value"}]*(int(n)+1-len(yAxis))
            yAxis[int(n)].update(in_yAxis.get(n))
            pass



    series=[]

    for r in in_series:

        # 多条y轴
        if r.get("yAxisIndex"):
            if len(yAxis) < r.get("yAxisIndex") + 1:
                yAxis = yAxis + [{"type": "value"}] * (r.get("yAxisIndex") + 1 - len(yAxis))

        serie={"name":None,"type":"line","data":[]}
        if "from" in r and "k" in r :
            r["name"]= explain[r.get("from")]["o"].get(r.get("k")).get("nm")
            if r.get("from") not in o_froms:
                o_froms[r.get("from")]=[r.get("k")]
            else:
                o_froms[r.get("from")].append(r.get("k"))
        serie.update(r)
        series.append(serie)
        pass

    a_datas={}
    # 将字段汇总
    for table,keys in o_froms.items():
        a_data = o_data.get(table) or []
        for d in a_data:
            for k in keys:
                k_v=d.get(k)
                if table+"_"+k not in a_datas:
                    a_datas[table+"_"+k ]=[]
                a_datas[table + "_" + k].append(k_v)

    xAxis["data"]=a_datas.get(xAxis.get("from")+"_"+xAxis.get("k"))
    for serie in series:
        serie["data"]=a_datas.get(serie.get("from")+"_"+serie.get("k")) or []

# legend
    legend={"data":[]}
    for serie in series:
        legend["data"].append(serie.get("name"))

    ret={"xAxis":xAxis,
         "yAxis":yAxis,
         "series":series,
         "legend":legend
         }         
    
    return ret
    

def chartSeriesbind(o_chart,**kwargs):
    pass
# open	float	开盘价
# high	float	最高价
# low	float	最低价
# close	float	收盘价
# pre_close	float	昨收价
# change	float	涨跌额
# pct_change	float	涨跌幅

    daily_color={
        "high":"#37c5ff",
        "close":"#f45200",
        "low":"#19cd85",
        "pct_change":"#b34775",
        "open":"#959595"
    }

    index_color = {

        "close": "#59fbd3"

    }

    for r in o_chart.get("series",[]):
        o_color=daily_color if r.get("from")=="daily" else index_color
        if r.get("k") in o_color:
            if "itemStyle" not in r:
                r["itemStyle"]={}
            r["itemStyle"]["color"]=o_color.get(r.get("k"))
    pass

# 横纵转换

def rowToChart(rows,x_axis,y_axis=[]):



    pass
    

''' 
# 该接口主要返回，单个股票的各项信息
{
    code:{ 
        records:[
            {"daily":{}, // 每日指标
             "daily_basic":{}//日线行情
            }
        ]
    }
} '''

def  StockRecordItems(items={},oBasic=None,time_q={},reverse=False,**kwArgs):
        if reverse:
            reverse=-1
        else:
            reverse=1

        record={}
        if oBasic:
            record["code"]=oBasic.get("ts_code")
            record["o_basic"]=oBasic
        explain={}
        if not items:
            items={
                "daily":{},
                "daily_basic":{},

                "index_daily":{"ts_code":"000008.SH"}
            }
        #     获取字段注释
        for s in items.keys():
            one_config=basic.pro_interface_config.get({"table_nm":s})
            one_o=basic.config_col_obj(one_config)
            if one_o and one_o.get("a"):
                explain[s]=one_o

        if  "daily" in items:
            l=daily.items(query=dict({"ts_code":oBasic.get("ts_code")},**time_q),_sort=[("ts_code",reverse)])
            record["daily"]=list(l)

        if  "daily_basic" in items:
            l=daily_basic.items(query=dict({"ts_code":oBasic.get("ts_code")},**time_q),_sort=[("ts_code",reverse)])
            record["daily_basic"]=list(l)

        if  "index_daily" in items:
            l=index_daily.items(query=dict({"ts_code":items.get("index_daily").get("ts_code")},**time_q),_sort=[("ts_code",reverse)])
            record["index_daily"]=list(l)
        return record  ,explain  

#  查询股票信息
def  StockHistorys(codes,s=None, e=None, interval="day",items=None,reverse=False,n=None,stock_query={},**kwArgs):
     
    #  时间查询条件
    time_q={}
    if s or e:
        time_q["trade_date"]={}
    if s:
        time_q["trade_date"]["$gte"]=s
    if e:
        time_q["trade_date"]["$lte"]=s
    if codes:
        stock_query["ts_code"]={"$in":codes}
    l=stock_basic.items(query=stock_query)
    # 此处是为了方便以后接入其他数据
    o={}
    explain=None
    #  该接口主要返回，单个股票的各项信息
    for r in l:
        one,explain=StockRecordItems(items=items,oBasic=r,time_q=time_q)
        o[r.get("ts_code")]=one

    ret={"explain":None,"a":[]}
    for s in codes:
        if s in o:
            ret["a"].append(o.get(s))
    ret["explain"]=explain
    return ret


''' 
param_chart
in_xAxis={"k":"字段","from":"哪个表里的字段"},in_yAxis={},
                in_series=[{"k":"","from":""}] '''
# 针对单个股票的图表
def getStockHistory_tochart(query_data,query_chart,**kwArgs):
    oData=StockHistorys(**query_data)
    chart={}
    if oData :
        for r in (oData.get("a",[]) or []):
            pass
            chart=rowToSimpleCharts(r,oData.get("explain"),**query_chart)
    # 显示格式处理
    chartSeriesbind(chart)        
    pass
    return chart



