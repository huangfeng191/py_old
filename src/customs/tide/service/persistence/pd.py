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
    def __init__(self,carousel,rule ,data=None):
        self.data=data
        self.carousel=carousel
        self.rule=rule
        self.df=None
    def tableToDataFrame(self):

        df = pd.DataFrame(list(self.data or []))
        self.df=df
        pass
    def do_subjoin(self,df):
        if df.empty:
            return None
        commands=self.rule.get("subjoin")
        out={}
        for r in self.rule.get("out").get("fields"):
            out[r]=0
        df['temp'] = df['change']
        df['pct_chg_5'] = df['pct_chg']
        out['up_percent_gt5'] =int( df.loc[df.loc[:, 'pct_chg'] >= 5, 'pct_chg'].count())
        out['down_percent_gt5'] = int(df.loc[df.loc[:, 'pct_chg'] <= -5, 'pct_chg'].count())
        out['limit_up'] = int(df.loc[df.loc[:, 'pct_chg'] >= 9.7, 'pct_chg'].count())
        out['limit_down'] = int(df.loc[df.loc[:, 'pct_chg'] == -9.7, 'pct_chg'].count())
        df.loc[df.loc[:, 'temp'] >= 0, 'temp'] = 1
        df.loc[df.loc[:, 'temp'] < 0, 'temp'] = 0
        df['c'] =((df['temp'].shift(1).fillna(0)) != df['temp']).cumsum()

        if not df[df.loc[:,"temp"]==1].empty:
           out['continue_up'] = int(df[df['temp'] == 1]['c'].value_counts().max())
        if not df[df.loc[:, "temp"] == 0].empty:
            out['continue_down'] = int(df[df['temp'] == 0]['c'].value_counts().max())
        out['ups'] = int(df[df['temp'] == 1]['c'].value_counts().sum())
        out['downs'] = int(df[df['temp'] == 0]['c'].value_counts().sum())
        out['ratio'] = round(float((df['close'].iloc[-1]) / df['close'].iloc[0]),3)
        # out['chain_ratio'] =round( float((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]),3)

        return out

    def go(self):
        self.tableToDataFrame()
        return self.do_subjoin(self.df)