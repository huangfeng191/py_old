
GBindings.push({
    Code: 'StorageWay',
    Desc:"(存储方式)在获取接口数据的时候，将数据存储的方式",
    Records: [
       { name: '新建表', value: '1' },
       { name: '数组对象', value: '2' },
       { name: 'Object对象', value: '3' }
    ]
   });



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
            nm:"", // 记录名
            oOne:{},
            columns:[],
            inputs:[],
            inputsRet:[[]],
            orders:[],
            quicks:[],
            props:[],
          
        };

      var p= co($.po("/prostock/interfaceconfig/query.json",{ query: {'table_nm':table_nm} },{"async":false})).done(function(json)
      {
        if(json.rows&&json.rows.length>0){
            // colInp 列定义
            if(json.rows[0].colInp){
                retO.nm=json.rows[0].nm;
                // 以下为处理列
                let tempStr=json.rows[0].colInp;
                let temp2a=tempStr.split("\n");// 字段数组
                    temp2a=temp2a.map(function(v){ //变为二维数组
                        if(v.split(",").length>1){
                            return v.split(",")
                        }else{
                            return v.split("：")
                        }
                    })
                //  开始解析字段处理逻辑
                //  数据格式：  sn ,dataType,nm,width
                    temp2a.forEach(element => {
                        var sn=element[0]||""
                        var nm=element[2]||""
                        var width=element[3]||"100";
                        var dataType="String";
                        if(element[1].includes["str","String","string"]){
                            dataType="String";
                        }
                        var showType="text";
                        var other={"columns":[],"inputs":[],"props":[],"quicks":[]};
                        let oDdic=GetBindRow(sn,"Relation");
                        if(oDdic){
                            showType="combo"
                            other["binding"]=oDdic.value;
                            other["columns"]=[`,"binding": "${other["binding"]}"`]
                            other["inputs"]=[`,"Ext": "${other["binding"]}"`]
                            other["props"]=[`,"Ext": "${other["binding"]}"`]
                            other["quicks"]=[`,"Ext": "${other["binding"]}"`,` "Source": "${other["binding"]}","TextField": "name", "ValueField": "value"`]
                        }
                      
                        // 保存字段配置
                        retO["oOne"][sn]={sn,dataType,nm,width,showType,other};

                        var templateCols=`{ "field": "${sn}","title":"${nm}","width":"${width}", "halign": "center" ${other["columns"].join(",")} }`;
                        var templateInputs=` { "Field": "${sn}", "Name": "${nm}", "ShowType":"${showType}" ${other["inputs"].join(",")} } `
                        var templateProps=`{ "Field":"${sn}", "Name" : "${nm}", "ShowType":"${showType}","DataType": "${dataType}" ,"FilterEnabled": true,"OrderEnabled": true ${other["props"].join(",")}  }`;
                        retO.columns.push(JSON.parse(templateCols))
                        retO.inputs.push(JSON.parse(templateInputs))
                        retO.props.push(JSON.parse(templateProps))
                    })


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
                        aQuicksStr=quicksStr.split("\n")
                        aQuicksStr.forEach(element => {
                            let sn=element.split(",")[0]||"";
                           if(retO["oOne"][sn]){
                               let nm=retO["oOne"][sn].nm;
                               let width=retO["oOne"][sn].width;
                               let dataType=retO["oOne"][sn].dataType;
                               let showType=retO["oOne"][sn].showType;
                               let type=(showType=="combo"?"QCombox":"QText");
                              
                               let other=retO["oOne"][sn].other;
                           
                            var templateQuicks=` { "Field": "${sn}", "Label": "${nm}",  "Type": "${type}", "Width": ${width} ${other["quicks"].join(",")} } `;
                           
                            
                            retO.quicks.push(JSON.parse(templateQuicks))
                           
                           }
                           
                        });
                       
                    }





            }
        }

    })
    //  input 处理分行
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