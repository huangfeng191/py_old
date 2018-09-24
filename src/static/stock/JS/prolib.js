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

function getBindConfig(){
    let p=co($.po("/prostock/interfaceconfig/query.json",{ query: {},order:[{"Field":"w", "Type": false}] },{"async":false})).done(function(json){
        if(json.rows&&json.rows.length>0){
            let records=[];  
            json.rows.forEach(element => {
                records.push({"name":element.nm,"value":element.table_nm})
            });
            GBindings.push({
                Code: 'StockConfig',
                Records: records
               });
        }
    });
  
}



function getInterfaceConfig({table_nm}){
        var retO={
            nm:"",
            oOne:{},
            columns:[],
            inputs:[],
            orders:[],
            quicks:[],
            inputsRet:[[]]
        };

      var p= co($.po("/prostock/interfaceconfig/query.json",{ query: {'table_nm':table_nm} },{"async":false})).done(function(json)
      {
          if(json.rows&&json.rows.length>0){
            if(json.rows[0].colInp){
                let tempStr=json.rows[0].colInp;
                temp2a=tempStr.split("\n");
                retO.nm=json.rows[0].nm
                temp2a=temp2a.map(function(v){
                    if(v.split(",").length>1){
                        return v.split(",")
                    }else{
                        return v.split("：")
                    }
                })
                temp2a.forEach(element => {
                    var sn=element[0]||""
                    // var tp=element[1]||""; 数据类型，暂时不用
                    var nm=element[2]||""
                    retO["oOne"][sn]={sn,nm}
                    var templateCols=`
                        { "field": "${sn}","title":"${nm}","width": 100, "halign": "center"}
                    `
                    var templateInputs=`
                    { "Field": "${sn}", "Name": "${nm}" }
                    `
                    retO.columns.push(JSON.parse(templateCols))
                    retO.inputs.push(JSON.parse(templateInputs))
                });
            }
            if(json.rows[0].orders){
                let ordersStr=json.rows[0].orders;
                aOrdersStr=ordersStr.split(",")
                aOrdersStr.forEach(element => {
                    let sn=element||""
                    var templateOrder=`
                    { "Field": "${sn}", "Type": false }
                   `
                   retO.orders.push(JSON.parse(templateOrder))
                });
               
            };
            if(json.rows[0].quicks){
                let quicksStr=json.rows[0].quicks;
                aQuicksStr=quicksStr.split(",")
                aQuicksStr.forEach(element => {
                    let sn=element||""
                    
                 
                   if(retO["oOne"][sn]){
                       let nm=retO["oOne"][sn].nm
                       var templateQuicks=`
                       { "Field": "${sn}", "Label": "${nm}",  "Type"   : "QText", "Width": 70 }
                      `
                    retO.quicks.push(JSON.parse(templateQuicks))
                   }
                   
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