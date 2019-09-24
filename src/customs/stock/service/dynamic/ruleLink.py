# -*- coding: UTF-8 -*-
# Module  : py
# Description :用规则调用的方法
# Author  : Wujj
# Date    : 2019/09/25
# Version : 1.0


from customs.stock.service.dynamic.ruleFun import *


@wrapper.calc_runtime_wrapper
def doLinkOne(linkId,**kwargs):
    pass
    # 此处记录日志
    # 告知输出从哪里去取以及 如何取
    link=dynamic_link.get(linkId)
    for one in link.get("cell",[]):
        one["logSource"] = "dynamic_link_cell_log"
        loadRule(**one)
    return "OK"



