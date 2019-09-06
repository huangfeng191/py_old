# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2019/09/01
# Version : 1.0
# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2019/09/01
# Version : 1.0
import ctx
from service import comm



dynamic_comm_test = comm.CRUD(ctx.dynamicdb, "test", [("method", 1)])
dynamic_comm_test_log = comm.CRUD(ctx.dynamicdb, "test_log", [("method", 1)])