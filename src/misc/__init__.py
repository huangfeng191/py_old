# -*- coding: utf-8 -*-
# Module  : 混杂的
# Author  : fengfeng
# Date    : 2017-7-15
# Version : 1.0
import logging
import time
import pymongo.helpers
import web
import ctx


LEVEL_USER  = 1
LEVEL_ADMIN = 8

# mongodb 添加索引
def indexing(db=None, *indexes):

    if ctx.ND_PREFIX != "":
      return lambda func: func

    if db and indexes:

      _indexes = set([]) if db.count() == 0 else db.index_information().keys()

      for idx in indexes:

        options = dict(idx).get('__options__', {})
        idx = [ k for k in idx if k[0] != '__options__']
        options['background'] = True

        name = pymongo.helpers._gen_index_name(idx)

        # if not ctx.rdb.sismember("%s:indexes" % (ctx.DB_PREFIX, ) , db.full_name + ":" + name):
        #
        #   now = time.time()
        #   logging.debug("Ensuring index %s->%s" % (repr(idx),repr(db)))
        #
        #   if name not in _indexes: db.ensure_index(idx, **options)
        #
        #   if time.time() - now > 1.0:
        #     logging.info("Ensured index %s->%s" % (repr(idx),repr(db)))
        #
        #   ctx.rdb.sadd("%s:indexes" % (ctx.DB_PREFIX, ) , db.full_name + ":" + name)

    return lambda func: func

class event(object):

    def __init__(self, func):
        self._key = func.__name__

    def __get__(self, obj, cls):

        if self._key not in obj.__dict__:
          obj.__dict__[self._key] = BindEvent()

        return obj.__dict__[self._key]

class BindEvent(object):

    def __init__(self):
        self._fns = []

    def __iadd__(self, fn):
        self._fns.append(fn)
        return self

    def __isub__(self, fn):
        self._fns.remove(fn)
        return self

    def __call__(self, *args, **kwargs):

        for f in self._fns[:]:
            f(*args, **kwargs)


def privileged(level):

    def _privileged(func):

        def __privileged(self, *args, **kwArgs):

          if level & LEVEL_ADMIN:

            admin = None

            if '_admin' in kwArgs:
              admin = kwArgs['_admin']
            else:
              sess = web.ctx.session
              admin = sess.get('admin', None)

            if not admin:
              raise web.notacceptable()

          if level & LEVEL_USER:

            admin = None
            user  = None

            if '_admin' in kwArgs:
              admin = kwArgs['_admin']
            else:
              sess = web.ctx.session
              admin = sess.get('admin', None)

            if '_user' in kwArgs:
              user = kwArgs['_user']
            else:
              sess = web.ctx.session
              user = sess.get('user', None)

            if not admin and not user:
              raise web.notacceptable()

          return func(self, *args,**kwArgs)

        return __privileged

    return _privileged
