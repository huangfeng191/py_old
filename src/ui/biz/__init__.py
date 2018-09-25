# -*- coding: utf-8 -*-
# Module  : ui.biz
# Author  : fengfeg
# Date    : 2018-09-25
from ui import path, CRUD,ArrayCRUD, wildcard
import web
from web.contrib.template import render_mako
import service.biz

render_biz = render_mako(directories=['templates/biz'],input_encoding='utf-8',output_encoding='utf-8',)


@path("/biz/ddic.html")
class BizData:

    def GET(self):

        return render_biz["ddic"]()

@wildcard("/biz/ddic/")
class BizDataCRUD(CRUD):

  def __init__(self):

    self.module = service.biz.ddics

@wildcard("/biz/ddic/record/")
class BizDataRecordCRUD(ArrayCRUD):

  def __init__(self):

    self.module = service.biz.ddics
    self.array = 'Records'