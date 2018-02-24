# -*- coding: UTF-8 -*-
# Module  : py
# Description :原始文件
# Author  : Wujj
# Date    : 2018-2-24
# Version : 1.0
import web
import json
import time
import re
from ui import path, CRUD, wildcard
from web.contrib.template import render_mako
from webservice import POST, GET



render_n = render_mako(directories=["customs/rabbit/templates", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")
@wildcard("/rabbit/admin/")
class RabbitAdminCRUD(CRUD):
    def __init__(self):
        self.module = rabbitadmin