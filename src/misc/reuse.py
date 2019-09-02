# -*- coding: utf-8 -*-
# Module  :
# Author  : fengfeng
# Date    : 2018-10-02
# Version : 1.0
# Desc    : 主要是自己写的方便函数
import utils
import time

# 组装默认参数，与传入合并
def bindReuse(params):
    if params and "date" in params:
        date = getParamsDateType()
        date.update(params.get("date"))
        params["date"] = date

    return params

def getParamsDateType():
    ret={"day":"","month":"","year":""}
    n=int(time.time())
    ret["day"]=utils.YMD(n,"%Y%m%d")
    ret["month"] =utils.YMD(n,"%Y%m")
    ret["year"] = utils.YMD(n,"%Y")
    return ret


