# -*- coding: utf-8 -*-
# Module  : 用户模块

import ctx
import service.comm as comm
# 　菜单定义
menus = comm.CRUD(ctx.cmdb, 'menu', [('sn', 1), ('lv', 1)], [('pid', 1), ('id', 1)], [('pid', 1), ('nm', 1)])

