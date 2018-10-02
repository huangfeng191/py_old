$.po = function (url,data, opts) {
    
    let _opts= {
         type:'POST',
         data:JSON.stringify(data),
         url:url,
         contentType:'application/json; charset=utf-8',
         dataType:'json'
     }
     return $.ajax($.extend({}, _opts, opts || {}));
 }
 
 function co(func) {
     var self=this;
     
     return $.Deferred(function(def){
         return func.then(function(rep){
             if(rep.Code == 0){
                 return def.resolve(rep.Response);
             }else{
                 return def.reject(rep.Response);
             }
         });
     });
 }