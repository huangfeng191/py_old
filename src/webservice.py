# -*- coding: UTF-8 -*-
# Module  : boot
# Description : 启动脚本
# web.py  2017-07-15
# Author  : fengfeng
# Date    : 2017-07-15
# Version : 1.0
import os
import site
# 添加临时环境变量 os.getcwd() 当前路径
site.addsitedir(os.path.join(os.getcwd(), '..', 'lib'))

import PlatLib  # 添加平台环境变量
#  暂时不用 ------------


import sys

reload(sys)
sys.setdefaultencoding("utf-8")  # @UndefinedVariable

import ui


# mongo 信息
import service  # @UnusedImport-


if __name__ == "__main__":
    ui.main()
