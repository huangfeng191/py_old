
var Prefix="";
$.po = function (url, data, opts) {
    let _opts = {
        type: 'POST',
        data: JSON.stringify(data),
        url: url,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json'
    }

    return $.ajax($.extend({}, _opts, opts || {}));
}

function co(func) {
    var self = this;
    return $.Deferred(function (def) {
        return func.done(function (rep) {
            if (rep.Code == 0) {
                return def.resolve(rep.Response);
            } else {
                return def.reject(rep.Message);
                // return def.reject(rep.Response);
            }
        }).fail(function (rep) {
            return def.reject(rep);
        });
    });
}


var stockService={

    // /dynamic/comm/test/log
    "dynamic":{
        "comm":{
            "testCRUD":CRUD("dynamic/comm/test"),
            "testLogCRUD":CRUD("dynamic/comm/test/log")
        },
        "setting":{
            "step":CRUD("dynamic/step"),
            "stepLink":CRUD("dynamic/step/link"),
            "link":CRUD("dynamic/link"),
            "linkCell":CRUD("dynamic/link/cell")
        }
       
    }

  
}


function CRUD(model,_prefix){
    var pre=_prefix||Prefix;
    var url=`/${model}`
    if(pre){
         url=`/${pre}/${model}`
    }
  
    var key="_id";
    return {
        query:(params)=>{return co($.po(`${url}/query.json`,params||{}))},
        insert:(record)=>{return co($.po(`${url}/insert.json`,{record:record}))},
        update:(record)=>{return co($.po(`${url}/update.json`,{record:record}))},
        save:(record)=>{
            if(record[key]){
                return co($.po(`${url}/update.json`,{record:record}));
            }else{
                return co($.po(`${url}/insert.json`,{record:record}));
            }
        },
        delete:(record)=>{return co($.po(`${url}/delete.json`,{record:record}))},
        get:(id)=>{return co($.po(`${url}/get.json`,id))},
       
        post:(m,record)=>{return co($.po(`${url}/${m}.json`,record))},
        key:key
    }
}
