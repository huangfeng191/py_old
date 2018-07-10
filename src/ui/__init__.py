# -*- coding: utf-8 -*-
# Module  : 开启web服务+导入modules
# Author  : lijiajie@chinahddz.com
# Date    : 2013-12-28
# Version : 1.0


import web
import sys
import misc
from webservice import POST, GET

from service.comm.mongo import MongoCRUD
# CRUD 使用
def wildcard(base, suffix='\.json'):
    return path(base + '([^/]+)' + suffix)


class CRUD(POST, GET):
    # @misc.privileged(misc.LEVEL_USER)  ------------
    def action(self, act, *args, **kwArgs):

        if act == 'update':
            return self.update(*args, **kwArgs)
        elif act == 'insert':
            return self.insert(*args, **kwArgs)
        elif act == 'delete':
            return self.delete(*args, **kwArgs)
        elif act == 'query':
            return self.query(*args, **kwArgs)
        elif act == 'get':
            return self.get(*args, **kwArgs)
        elif act == 'index':
            return self.index(*args, **kwArgs)
        elif act == 'importing':
            return self.importing(*args, **kwArgs)
        elif act == 'exporting':
            return self.exporting(*args, **kwArgs)

        raise Exception("Unsupported Operation")

    def update(self, record=None, records=None, *args, **kwArgs):

        if record:
            return self.module.upsert(_action='update', **record)

        if records:
            return map(self.update, records)

        raise Exception('无效更新!')

    def insert(self, record=None, records=None, *args, **kwArgs):

        if record:
            return self.module.upsert(_action='insert', **record)

        if records:
            return map(self.insert, records)

        raise Exception('无效插入!')

    def delete(self, record=None, *args, **kwArgs):

        self.validate(record, *args, **kwArgs)

        if record:
            return self.module.delete(record.get('_id'), record=record, *args, **kwArgs)

        raise Exception("非法删除")

    def query(self, count=True, *args, **kwArgs):

        cs = self.module.items(*args, **kwArgs)

        if not isinstance(self.module, MongoCRUD):
            return cs

        total = None

        if count:
            total = cs.count()

        return {
            'total': total,
            'rows': list(cs)
        }

    def get(self, *args, **kwArgs):
        if '_cid' in kwArgs:
            del kwArgs['_cid']
        if '_customer' in kwArgs:
            del kwArgs['_customer']
        return self.module.get(*args, **kwArgs)

    def validate(self, record=None, *args, **kwArgs):
        return True

    def importing(self, src=None, *args, **kwArgs):
        raise Exception("功能未支持!")

    def exporting(self, model=None, *args, **kwArgs):
        raise Exception("功能未支持!")


urls = ()


def path(*uris):
    class ClassWrapper:
        def __init__(self, cls):
            global urls
            for uri in uris:
                urls += (uri, cls)
            self.other_class = cls

        def __call__(self, *args, **kwArgs):
            return self.other_class(*args, **kwArgs)

    return ClassWrapper


def _cookie_name():
    if web.ctx.host and ':' in web.ctx.host:
        return 'sid' + web.ctx.host.split(':')[1]
    return 'sid'


# 导入模块
import modules


import misc.mongos



def main(argv=None):
    argv = argv or sys.argv
    web.config.session_parameters['cookie_name'] = _cookie_name
    web.config.debug = False
    web.config.session_parameters['cookie_domain'] = None
    web.config.session_parameters['timeout'] = 30 * 24 * 3600
    web.config.session_parameters['secret_key'] = 'FENGFENG'
    web.config.session_parameters['cookie_path'] = '/'
    port = 8080
    if len(argv) > 1:
        port = int(argv[1])

    app = web.application(urls, globals())
    app.notfound = lambda: web.seeother("/static/notfound.html")

    

    app.run()
