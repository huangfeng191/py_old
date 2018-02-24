# -*- coding: UTF-8 -*-
# Module  : py
# Description :原始文件
# Author  : Wujj
# Date    : 2018-2-24
# Version : 1.0
import web
import json
import time
from bson import ObjectId
import re
from copy import deepcopy
from ui import path, CRUD, wildcard
from web.contrib.template import render_mako
from webservice import POST, GET
from ui.biz

import BizDepsTree, UBizBindings
import service.biz

from ui.scada import _parse_conditions
from customs.jinan.service import *
from misc import customize, authorize, privileged, rolize, userize, streecid, \
    tokenize, utils

render_n = render_mako(directories=["customs/jinan/templates", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")
$MY_VARIABLE$ $END$ 