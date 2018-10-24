# -*- coding: UTF-8 -*-
# Description : proapi 报表
# Author  : fengfeng
# Date    : 2018/10/24
# Version : 1.0



import tushare_proapi
# 已时间为记录
def rowToO(table_name,x_axis=[],y_axis=[],query=None):
    
    rows=eval(table_name).items(query=query,fields=set(x_axis+y_axis))

    
    pass


# 横纵转换

def rowToChart(rows,x_axis,y_axis=[]):
    pass
    



