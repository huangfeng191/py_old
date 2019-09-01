# -*- coding: UTF-8 -*-
# Module  : py
# Description :实际对象
# Author  : Wujj
# Date    : 2019/08/31
# Version : 1.0
# -*- coding: UTF-8 -*-
# Module  : py
# Description :实际对象
# Author  : Wujj
# Date    : 2019/08/31
# Version : 1.0
import ctx

from service import comm


# 获取股票基本信息
stock_basic = comm.CRUD(ctx.tuprodb, "stock_basic", [("ts_code", 1)])
# 沪深股通成份股
hs_const = comm.CRUD(ctx.tuprodb, "hs_const", [("ts_code", 1)])
# 股票曾用名
namechange = comm.CRUD(ctx.tuprodb, "namechange", [("ts_code", 1)])

# 行情数据
# 日线行情
daily = comm.CRUD(ctx.tuprodb, "daily", [("ts_code", 1),("trade_date",1)])
# 复权因子
adj_factor = comm.CRUD(ctx.tuprodb, "adj_factor", [("ts_code", 1),("trade_date",1)])
# 停复牌信息
suspend = comm.CRUD(ctx.tuprodb, "suspend", [("ts_code", 1)])
# 每日指标
daily_basic = comm.CRUD(ctx.tuprodb, "daily_basic", [("ts_code", 1)])

# 财务数据
# 利润表
income = comm.CRUD(ctx.tuprodb, "income", [("ts_code", 1)])
# 业绩快报
express = comm.CRUD(ctx.tuprodb, "express", [("ts_code", 1)])
# 财务指标数据
fina_indicator = comm.CRUD(ctx.tuprodb, "fina_indicator", [("ts_code", 1)])
# 主营业务构成
fina_mainbz = comm.CRUD(ctx.tuprodb, "fina_mainbz", [("ts_code", 1)])
# 主营业务构成
fina_mainbz = comm.CRUD(ctx.tuprodb, "fina_mainbz", [("ts_code", 1)])


# 指数基本信息
index_basic = comm.CRUD(ctx.tuprodb, "index_basic", [("ts_code", 1)])
# 指数日线行情
index_daily = comm.CRUD(ctx.tuprodb, "index_daily", [("ts_code", 1),("trade_date",1)])





# 获取上市公司基础信息
stock_company = comm.CRUD(ctx.tuprodb, "stock_company", [("ts_code", 1)])
