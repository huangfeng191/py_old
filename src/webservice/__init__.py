# -*- coding: UTF-8 -*-
# Module  : webservice
# Description :  WebService Layer
# Author  : lijiajie@chinahddz.com
# Date    : 2014-05-04
# Version : 1.0




class POST:
    def action(self, *args, **kwArgs):
        raise NotImplementedError();

    def POST(self, *args, **kwArgs):
        return self.action(*args, **kwArgs)


class GET:
    def action(self, *args, **kwArgs):
        raise NotImplementedError();

    def GET(self, *args, **kwArgs):
        return self.action(*args, **kwArgs)
