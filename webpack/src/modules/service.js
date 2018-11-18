var Prefix = '';

$.po = function (url,data) {
    return $.ajax({
        type:'POST',
        data:JSON.stringify(data),
        url:url,
        contentType:'application/json; charset=utf-8',
        dataType:'json'
    })
}

$.ge = function (url) {
    return $.ajax({
        type:'GET',
        url:url,
        contentType:'application/json; charset=utf-8',
        dataType:'json'
    })
}

function co(func) {
    var self=this;
    return $.Deferred(function(def){
        return func.then(function(rep){
            if(rep.Code == 0){
                return def.resolve(rep.Response);
            }else{
                window.App.$message.error(rep.Message||"调用过程发生错误");
                return def.reject(rep);
            }
        });
    });
}

export function CRUD(service,model){
    var qurl=`/${service}/${model}/query.json`;
    return {
        query:(params)=>{return co($.po(qurl,params))},
        insert:(record)=>{return co($.po(`/${service}/${model}/insert.json`,{record:record}))},
        update:(record)=>{return co($.po(`/${service}/${model}/update.json`,{record:record}))},
        delete:(record)=>{return co($.po(`/${service}/${model}/delete.json`,{record:record}))},
        get:(id)=>{return co($.po(`/${service}/${model}/get.json`,{_id:id||{}}))},
        post:(m,params)=>{return co($.po(`/${service}/${model}/${m}.json`,params))},
        url:qurl,
        key:"_id"
    }
};

export const API = {
    Load:(url, param)=>{
        return co($.po(Prefix+url, param));
    },
    getStaticMd:(param)=>{
        return co($.po(Prefix+"/biz/markdown/get_static_md.json", param));
    },

};
