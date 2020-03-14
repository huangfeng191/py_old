# -*- coding: UTF-8 -*-
# Module  : py
# Description :生成数据-实体
# Author  : Wujj
# Date    : 2020/1/31
# Version : 1.0


import ctx
from service import comm


tide_daily_cell= comm.CRUD(ctx.tide_outDb, "daily_cell", [("ts_code", 1)]) # 明细
tide_daily_link= comm.CRUD(ctx.tide_outDb, "daily_link", [("ts_code", 1)])
tide_daily_step= comm.CRUD(ctx.tide_outDb, "daily_step", [("ts_code", 1)])
tide_daily_measure= comm.CRUD(ctx.tide_outDb, "daily_measure", [("ts_code", 1)])
tide_daily_plan= comm.CRUD(ctx.tide_outDb, "daily_plan", [("ts_code", 1)])


tide_basic_cell= comm.CRUD(ctx.tide_outDb, "basic_cell", [("ts_code", 1)]) # 明细
tide_basic_link= comm.CRUD(ctx.tide_outDb, "basic_link", [("ts_code", 1)])
tide_basic_step= comm.CRUD(ctx.tide_outDb, "basic_step", [("ts_code", 1)])
tide_basic_measure= comm.CRUD(ctx.tide_outDb, "basic_measure", [("ts_code", 1)])
tide_basic_plan= comm.CRUD(ctx.tide_outDb, "basic_plan", [("ts_code", 1)])


tide_statistic_cell= comm.CRUD(ctx.tide_outDb, "statistic_cell", [("ts_code", 1)]) # 明细
tide_statistic_link= comm.CRUD(ctx.tide_outDb, "statistic_link", [("ts_code", 1)])
tide_statistic_step= comm.CRUD(ctx.tide_outDb, "statistic_step", [("ts_code", 1)])
tide_statistic_measure= comm.CRUD(ctx.tide_outDb, "statistic_measure", [("ts_code", 1)])
tide_statistic_plan= comm.CRUD(ctx.tide_outDb, "statistic_plan", [("ts_code", 1)])




tide_daily_business= comm.CRUD(ctx.tide_outDb, "daily_business", [("ts_code", 1)]) # 明细
tide_basic_business= comm.CRUD(ctx.tide_outDb, "basic_business", [("ts_code", 1)])
