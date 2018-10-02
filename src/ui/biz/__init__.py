# -*- coding: utf-8 -*-
# Module  : ui.biz
# Author  : fengfeg
# Date    : 2018-09-25
from ui import path, CRUD,ArrayCRUD, wildcard,POST
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



#menu




@path("/biz/menu.html")
class BizMenu:

    def GET(self):
         return render_biz["menu"]()



# simple tree
@path("/biz/menu/simple.json")
class BizMenuSimple(POST):

    def action(self, *args, **kwArgs):
        cs = []
        _cid = kwArgs.get('_cid')
        o = [{"id":_cid,"nm": u"所有菜单","open":True, 'isParent': True}]
        for c in cs:
          oo = {'isParent':True, 'id':c.get('_id'), 'sn':c.get('sn'), 'pid': c.get('pid'), 'nm': c.get('nm','-')}

          if c.get('pid',_cid) == _cid:
            oo['open'] = True
          else:
            oo['isParent'] = False
          o.append(oo)

        return o

@path("/biz/menu/tree.json")
class BizMenuTree(POST):

  def set_subMenus(self,id, menus):
      """
          根据传递过来的父菜单id，递归设置各层次父菜单的子菜单列表
      :param id: 父级id
      :param menus: 子菜单列表
      :return: 如果这个菜单没有子菜单，返回None;如果有子菜单，返回子菜单列表
      """
      # 记录子菜单列表
      Children = []
      # 遍历子菜单
      for m in menus:
          if m.get("pid") == id:
              Children.append(m)

      # 把子菜单的子菜单再循环一遍
      for sub in Children:
          menus2 =list(service.biz.menus.items(query={"pid":sub.get("_id")},fields=["_id","pid","nm","keep","sn","val","open","icon","target","display"],_sort=[("w",1)]))
          for menusr in menus2:
              menusr["Id"]=menusr.get("_id")
          # 还有子菜单
          if len(menus):
              sub["Children"] = self.set_subMenus(sub.get("_id"), menus2)

      # 子菜单列表不为空
      if len(Children):
          return Children
      else: # 没有子菜单了
          return None


  def action(self, *args, **kwArgs):
      cid = kwArgs.get('cid')
      o ={"_id":cid,"pid":"0","sn":"0","nm": u"所有菜单","open":True, 'isParent': True,"Children":[]}
      l =list(service.biz.menus.items(query={"pid":cid},fields=["_id","pid","nm","keep","sn","val","open","icon","target","display"],_sort=[("w",1)]))
      for r in l:
          r["Id"]=r.get("_id")
      subMenus=self.set_subMenus(cid,l)
      o["Children"]=subMenus
      return o


@wildcard("/biz/menu/")
class BizMenuCRUD(CRUD):
      
  def __init__(self):

      self.module = service.biz.menus
