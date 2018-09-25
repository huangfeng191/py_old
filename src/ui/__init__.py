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
from bson.objectid import ObjectId
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

class ArrayCRUD(CRUD):
    
  def insert(self, record=None, **kwArgs):

        if record:

          pid = record.pop("__pid")

          if pid is None:
            raise Exception("非唯一条件指定！")

          rs = self.module.items(size=2, conditions=[{'Field':"_id",'Operate':"=",'Value':pid,'Relation':"and"}],fields=[self.array])
          rs = list(rs)

          if len(rs) != 1:
            raise Exception("非法插入！")

          record["_id"] = str(ObjectId())
          self.module.upsert(pid, **{"$push":{self.array:record}})

          return record

        raise Exception("非法插入!")

  def update(self, record=None, **kwArgs):

        if record:

          pid = record.pop("__pid")

          if pid is None:
            raise Exception("非唯一条件指定！")

          _id = record.get('_id')

          if _id is None:
            raise Exception("非法更新！")

          rs = self.module.items(size=2, conditions=[{'Field':"_id",'Operate':"=",'Value':pid,'Relation':"and"},{'Field':("%s._id"%self.array),'Operate':"=",'Value':_id,'Relation':"and"}],fields=['%s.$'%self.array])
          rs = list(rs)

          if len(rs) != 1:
            raise Exception("非法更新！")

          if rs and len(rs) > 0 and self.array in rs[0]:

            for item in (rs[0][self.array] or []):

              if item and '_id' in item and item['_id'] == _id:

                for k,v in item.items():
                  if record and k not in record:
                    record[k] = v

          self.module.upsert(pid, _query={("%s._id"%self.array):_id}, **{"$set":{("%s.$"%self.array):record}})
          return record

        return record

  def delete(self, record=None, **kwArgs):

        if record:

          pid = record.pop("__pid")

          if pid is None:
            raise Exception("非唯一条件指定！")

          _id = record.pop('_id')

          if not self.module.exists(pid):
            raise Exception('非法删除!')
          else:
            self.module.upsert(pid, ** {"$pull":{self.array:{"_id":_id}}})

  def query(self, conditions=None, size=None, index=None, *args, **kwArgs):

        if conditions is None:
          raise Exception("非唯一条件指定！")

        mq = {}

        if conditions:

          cs = [c for c in conditions if c.get('Field') == '__pid']
          conditions = [c for c in conditions if c.get('Field') != '__pid']

          if cs and len(cs) == 1 :
            mq = {'_id': cs[0].get("Value")}
          else:
            raise Exception("__pid 未指定！")


        if len(conditions) > 0:
          fields = {self.array: {'$elemMatch':self.module.query(conditions)}}
        else:
          fields = [self.array]

        rs = self.module.items(size=2, query=mq,fields=fields)
        rs = list(rs)

        if len(rs) > 1:
          raise Exception("返回值不唯一")

        if len(rs) == 1:
          rs = rs[0].get(self.array, []) or []

        rs.sort(key=lambda x:(x.get('w'), x.get('_id')))

        total = len(rs)
        offset  = 0 if index == 0 else (index-1)*size
        rs = rs[offset : offset + size]

        return {
          'total': total,
          'rows': rs
        }

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
