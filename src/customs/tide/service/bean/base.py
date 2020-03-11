# -*- coding: UTF-8 -*-
# Module  : py
# Description :规则实体
# Author  : Wujj
# Date    : 2020/1/31
# Version : 1.0


import ctx
from service import comm

tide_cell = comm.CRUD(ctx.tide_baseDb, "cell" )
tide_link = comm.CRUD(ctx.tide_baseDb, "link" )
tide_step = comm.CRUD(ctx.tide_baseDb, "step" )
tide_measure = comm.CRUD(ctx.tide_baseDb, "measure" )
tide_plan = comm.CRUD(ctx.tide_baseDb, "plan" )

tide_chains_log = comm.CRUD(ctx.tide_baseDb, "chains_log" )


tide_cell_log = comm.CRUD(ctx.tide_baseDb, "cell_log" )
tide_link_log = comm.CRUD(ctx.tide_baseDb, "link_log" )
tide_step_log = comm.CRUD(ctx.tide_baseDb, "step_log" )
tide_measure_log = comm.CRUD(ctx.tide_baseDb, "measure_log" )
tide_plan_log = comm.CRUD(ctx.tide_baseDb, "plan_log" )


tide_journal_log= comm.CRUD(ctx.tide_baseDb, "journal_log" )
