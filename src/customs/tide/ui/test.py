# -*- coding: UTF-8 -*-
# Module  : py
# Description :测试
# Author  : Wujj
# Date    : 2020/2/3
# Version : 1.0

import re
import time
from misc import utils
from ui import path, wildcard, CRUD, ArrayCRUD
from web.contrib.template import render_mako
from webservice import POST
import customs.xining.service.building  as xiningbuilding
import service.biz as Biz
from ui.scada import _parse_conditions

render_building = render_mako(directories=["customs/xining/templates/building", "templates"], input_encoding="utf-8",
                              output_encoding="utf-8")
from bson.objectid import ObjectId
