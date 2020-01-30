# -*- coding: UTF-8 -*-
# Module  : py
# Description :生成数据-实体
# Author  : Wujj
# Date    : 2020/1/31
# Version : 1.0


import ctx
from service import comm


tide_daily= comm.CRUD(ctx.tide_outDb, "daily") # 明细
tide_basic= comm.CRUD(ctx.tide_outDb, "basic") 