# -*- coding: UTF-8 -*-
# Module  : py
# Description :pandas
# Author  : Wujj
# Date    : 2020/3/13
# Version : 1.0

import pandas as pd


from customs.stock.service.tushare_beans import *
from customs.tide.service.utils import *
from customs.tide.service.bean.base import *
from customs.tide.service.bean.out import *


class PandasDo:
    def __init__(self, source,carousel,rule):
        self.source=source
        self.carousel=carousel
        self.rule=rule
    def tableToDataFrame(self):
        l=index_basic.items()
        df = pd.DataFrame(list(l))
        pass
    def go(self):
        self.tableToDataFrame()