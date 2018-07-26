# -*- coding: UTF-8 -*-
# Module  : webservice
# Description :  WebService Layer
# Author  : lijiajie@chinahddz.com
# Date    : 2014-05-04
# Version : 1.0

import web
from urllib import unquote
import json
from collections import OrderedDict
import logging
from webservice.api.exception import RetException
# JSON-RPC WebService
def jws(func):
    def __decor(self, *args, **kwArgs):

        cbk = None
        method = web.ctx.env['REQUEST_METHOD']

        if method == 'GET':
            vals = web.input(data=None)
            if '__callback' in vals:
                cbk = vals['__callback']
                data = unquote(vals['data'])
            else:
                data = unquote(web.ctx.env['QUERY_STRING'])

        elif method == 'POST':
            data = web.data()

        try:
            if data == '':
                data = {}
            else:
                data = json.loads(data)
            r = json.dumps(OrderedDict([("Code", 0), ("Message", "OK"), ("Response", func(self, *args, **data))]))
        except RetException, e:
            logging.exception(e);
            r = json.dumps(OrderedDict([("Code", e.code), ("Message", e.msg), ("Response", {})]))
        except Exception, e:
            logging.exception(e);
            r = json.dumps(OrderedDict([("Code", 99999), ("Message", str(e)), ("Response", {})]))
        if cbk:
            web.header("Content-Type", "application/javascript; charset=UTF-8")
            return "".join([cbk, '(', r, ')'])

        web.header("Content-Type", "application/json; charset=UTF-8")
        return r

    return __decor


class POST:
    def action(self, *args, **kwArgs):
        raise NotImplementedError();

    @jws
    def POST(self, *args, **kwArgs):
        return self.action(*args, **kwArgs)


class GET:
    def action(self, *args, **kwArgs):
        raise NotImplementedError();

    @jws
    def GET(self, *args, **kwArgs):
        return self.action(*args, **kwArgs)
