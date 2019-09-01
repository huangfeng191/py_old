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
import logging
from misc import utils
import time
from datetime import datetime
from service import comm
from bson import ObjectId

xining_barcode = comm.CRUD(ctx.customdb, "xining_barcode", [("cid", 1)])