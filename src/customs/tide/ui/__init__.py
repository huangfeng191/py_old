# -*- coding: UTF-8 -*-
# Module  : py
# Description :
# Author  : Wujj
# Date    : 2020/1/31
# Version : 1.0


from ui import wildcard,CRUD,path


from web.contrib.template import render_mako
render_tide= render_mako(directories=["customs/tide/templates/", "templates"], input_encoding="utf-8",
                       output_encoding="utf-8")

import customs.tide.ui.base
import customs.tide.ui.comm
import  customs.tide.ui.log
import  customs.tide.ui.test
