
# -*- coding: UTF-8 -*-
# Module  : py
# Description :模块配置功能
# Author  : Wujj
# Date    : 2017-11-5
# Version : 1.0


import ctx
from copy import deepcopy
from service import comm


# 接口数据参数配置
# 最小单位是表  table_nm
pro_interface_config = comm.CRUD(ctx.tuprodb, "interface_config" )

pro_interface_log = comm.CRUD(ctx.tuprodb, "interface_log" )




# 多接口配置
pro_multi_data = comm.CRUD(ctx.tuprodb, "multi_data" )


# 将 interface_config 里面的是列转换成字段

def config_col_obj(config_row,field="colInp"):
    
    data_dict={
        "str":"String",
        "float":"Number",
        "default":"String"
    }

    show_dict={
        "d":"datetime",
        "c":"combo",
        "default":"text"
    }
    oRet={"a":[],"o":{}}

    for r in config_row.get(field).split("\n"):

        o = {"code": None,"dataType": None, "nm": None,  "showType": None, "binding": None, "format": None}
        fill=[None]*2
        ra=str.split(r,",")+fill

        code,dataType,nm,showType,other=ra[0:5]
        binding,format=None,None

        if not dataType:
            dataType=data_dict.get("default")
        if not showType:
            showType=show_dict.get("default")


        if dataType and data_dict.get(dataType):
            dataType= data_dict.get(dataType)

        if showType and show_dict.get(showType):
            showType = show_dict.get(showType)

        if other:
            if showType=="combo":
                binding=other
            elif showType=="datetime":
                format=other
        o = {"code": code, "dataType": dataType, "nm": nm, "showType": showType, "binding": binding, "format": format}
        oRet["a"].append(o)
        oRet["o"][code]=o

    return oRet


