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





function getInterfaceConfig({table_name="stock_basics"}){
        var retO={
            columns:[],
            inputs:[],
            inputsRet:[[]]
        };

      var p= co($.po("/stock/interfaceconfig/query.json",{ query: {'table_nm':table_name} },{"async":false})).done(function(json)
      {
          if(json.rows&&json.rows.length>0){
            if(json.rows[0].colInp){
                let tempStr=json.rows[0].colInp;
                temp2a=tempStr.split("\n");
                temp2a=temp2a.map(function(v){return v.split(",")})
                temp2a.forEach(element => {
                    var sn=element[0]||""
                    var nm=element[1]||""
                    
                    var templateCols=`
                        { "field": "${sn}","title":"${nm}","width": 100}
                    `
                    var templateInputs=`
                    { "Field": "${sn}", "Name": "${nm}" }
                    `

                    retO.columns.push(JSON.parse(templateCols))
                    retO.inputs.push(JSON.parse(templateInputs))
                });
            }
          }
      })
      let oneRow=[]
      retO.inputs.forEach(function(v,i){
        oneRow.push(v);
        if( oneRow.length>0&&oneRow.length%3==0){
            retO.inputsRet.push(oneRow)
            oneRow=[]
        }  
      })
      if(oneRow.length>0){
        retO.inputsRet.push(oneRow)
      }
      
      return retO
}