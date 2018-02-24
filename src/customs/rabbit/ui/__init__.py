# -*- coding: UTF-8 -*-
# Module  : py
# Description :原始文件
# Author  : Wujj
# Date    : 2018-2-24
# Version : 1.0

from ui import path, CRUD, wildcard
from web.contrib.template import render_mako
from customs.rabbit.service import  *


render_rabbit = render_mako(directories=["customs/rabbit/templates", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")
@wildcard("/rabbit/admin/")
class RabbitAdminCRUD(CRUD):
    def __init__(self):
        self.module = rabbit_admin

@path("/rabbit/admin.html")
class RabbitAdmin:
    def GET(self, _cid = None, *args, **kwargs):
        return render_rabbit["admin"]()

