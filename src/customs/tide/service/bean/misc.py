# -*- coding: UTF-8 -*-
# Module  : py
# Description :规则实体
# Author  : Wujj
# Date    : 2020/1/31
# Version : 1.0


import ctx
from service import comm

tide_test = comm.CRUD(ctx.tide_baseDb, "test" )
tide_test_log = comm.CRUD(ctx.tide_baseDb, "test_log" )