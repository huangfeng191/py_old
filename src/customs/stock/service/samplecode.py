# -*- coding: utf-8 -*-
from dataapi import Client
if __name__ == "__main__":
    try:
        client = Client()
        client.init('13d3ae777dfca314b3cfcabe0b6ae7c228e793dfd347ea41b2aba63660c2f1ff')
        url1='/api/equity/getEqu.json?field=&listStatusCD=&secID=&ticker=&equTypeCD=A'
        code, result = client.getData(url1)
        if code==200:
            print result
        else:
            print code
            print result

    except Exception, e:
        #traceback.print_exc()
        raise e