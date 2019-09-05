# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2019/08/24
# Version : 1.0
# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2019/08/24
# Version : 1.0
import ctx
import logging
from misc import utils
import time
from datetime import datetime
from service import comm
from bson import ObjectId

from service import comm


dynamic_step = comm.CRUD(ctx.dynamicdb, "step", [("cid", 1)])

dynamic_link = comm.CRUD(ctx.dynamicdb, "link", [("cid", 1)])
dynamic_link_log = comm.CRUD(ctx.dynamicdb, "link_log", [("cid", 1)])
dynamic_link_cell_log = comm.CRUD(ctx.dynamicdb, "cell_log", [("cid", 1)])



