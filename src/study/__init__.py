# -*- coding: utf-8 -*-
import mytime
import myrequires


local_host="http://127.0.0.1:8080"
url_path="/ubiz/user/get.json"

test_url="%s%s"%(local_host,url_path)

if __name__ == "__main__":
    # print  mytime.getFormatterDate()
    # scada  sandy Token 5b44546bb5c8536e6483b4fd

    params = {"_id": "59a3d2cdb5c85305a06b16f5"}
    params["_cid"]="59a3d272b5c85305a06b15df"
    sContent=myrequires.toPostUrl(test_url,params)
    if sContent.get("status")=="OK":
       print sContent
