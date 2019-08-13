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



export const stockService = {
    "getPoint":function(){
        var  url="/prostock/interfacedata/query.json?table_nm=stock_company";
       return co($.po(url)) 
     }

};
