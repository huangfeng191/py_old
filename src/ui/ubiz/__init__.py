# -*- coding: utf-8 -*-
# Module  : ui.biz
# Author  : fengfeg
# Date    : 2018-09-25
from ui import path, CRUD,ArrayCRUD, wildcard,POST
import web
from web.contrib.template import render_mako
import service.biz
from ui.biz import BizMenuTree
render_biz = render_mako(directories=['templates/biz'],input_encoding='utf-8',output_encoding='utf-8',)

