function showDialogList(idx,table_nm,s_query,url="/prostock/dlginterfacedata.html"){
    
    var row=PCRUD.View.Grid.Element.datagrid("getRows")[idx];
    
    var query={}
    query[s_query]=row[s_query];
    var config = {
        Title: "详细 "+table_nm, Url: url,
         Width: "1200", Height: "700",
         CloseButton: true
                };
        Dialog(config,{row,table_nm,query},function(res){
                
            });   
}

function showDialogChart(idx,table_nm=null,s_query,url="/stock/onechart.html"){
    debugger
    var row=PCRUD.View.Grid.Element.datagrid("getRows")[idx];
    
    var query={}
    query[s_query]=row[s_query];
    var config = {
        Title: "详细 "+table_nm, Url: url+"?code="+row[s_query]+"&table_nm="+table_nm,
         Width: "1200", Height: "700",
         CloseButton: true
                };
        Dialog(config,{query},function(res){
                
            });   
}



GBindings.push({
    Code: 'StorageWay',
    Desc:"(存储方式)在获取接口数据的时候，将数据存储的方式",
    Records: [
       { name: '新建表', value: '1' },
       { name: '数组对象', value: '2' },
       { name: 'Object对象', value: '3' }
    ]
   });

GBindings.push({
    Code: 'SendWay',
    Desc:"发送方式，",
    Records: [
       { name: '全部下载', value: 'all' },
       { name: '增量下载', value: 'increase' } 
    //    { name: 'Object对象', value: '3' }
    ]
   });
GBindings.push({
    Code: 'SendState',
    Desc:"发送方式，",
    Records: [
       { name: '启动', value: '0' },
       { name: '处理中', value: '1' },
       { name: '处理完成', value: '2' } 
    //    { name: 'Object对象', value: '3' }
    ]
   });

   GBindings.push({
    Code: 'GetCycle',
    Desc:"获取周期,",
    Records: [
       { name: '小时', value: 'hour',desc:"" },
       { name: '天', value: 'day',desc:"" },
       { name: '月', value: 'month' ,desc:""}, 
       { name: '年', value: 'year' ,desc:""} 

    //    { name: 'Object对象', value: '3' }
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
                records.push({"name":element.nm,"value":element.table_nm,"other":element.sendway})
            });
            GBindings.push({
                Code: 'StockConfig',
                Records: records
               });
        }
    });
  
}
function getMultDataTree(sid,callback){
    let nodes=[];
    let p=co($.po("/prostock/multiconfig/basetree.json",{sid},{"async":false})).done(function(arr){
        if(arr&&arr.length>0){
            nodes= arr||[];
            callback(nodes)
        }
    });
   
}


function getInterfaceConfig({table_nm,multi_sn}){
        var retO={
            nm:"", // 记录名
            oOne:{},
            columns:[],
            foreignCols:[],
            inputs:[],
            inputsRet:[],
            orders:[],
            quicks:[],
            props:[],

          
        };
        if(multi_sn){
            url=   "/prostock/multiconfig/getConfigs.json";
            query={'multi_sn':multi_sn}
        }else{
            url=   "/prostock/interfaceconfig/query.json";
            query={'table_nm':table_nm}
        }
    
      var p= co($.po(url,{ query},{"async":false})).done(function(json)
      {
        if(json.rows&&json.rows.length>0){
            // colInp 列定义
            if(json.rows[0].colInp){
                retO.nm=json.rows[0].nm;
                // 基础对象
                retO.basic=json.rows[0].basic||table_nm;
                retO.foreignCols=json.rows[0].foreignCols;
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
                //  数据格式：  sn ,dataType,nm,width,RowSpan=2,last:d  日期类型
                // 此参数暂时没用到
                var ddic_param={}
                    temp2a.forEach(element => {
                        var sn=element[0]||""
                        var nm=element[2]||""
                        var width=element[3]||"100";
                        var ddic_param_in=element[4]||""
                            ddic_param[sn]={}
                       
                        if(ddic_param_in && ddic_param_in.split("&").length>0){
                            $.each(ddic_param_in.split("&"),function(dpi,dpv){
                                if(dpv.split("=").length>1){
                                    ddic_param[sn][dpv.split("=")[0]]=dpv.split("=")[1]
                                }
                            })
                        }
                        var last_type= element.pop()
                        // 


                        var dataType="String";
                        if(element[1].includes["str","String","string"]){
                            dataType="String";
                        }
                        var showType="text";
                        if (last_type=="d"){
                            if(width=="d"){
                                width="100"
                            }
                            dataType="DateTime"
                        }else if(last_type=="a"){
                            showType="textarea";
                            // 
                        }else{
                            last_type=""
                            
                        }
                        var other={"columns":[],"inputs":[],"props":[],"quicks":[]};
                        var bindcode;
                        if(table_nm){
                             bindcode=GetBindCode({"Code":sn.split(".").pop(),"Basic":table_nm})
                        }else{
                            // 此处有问题
                            var a_bar_middle=sn.split(".");
                             bindcode=a_bar_middle.pop();
                             bindcode=GetBindCode({"Code":bindcode,"Basic":a_bar_middle.pop()||retO.basic });
                        }
                      
                        if(bindcode){
                            showType="combo"
                            other["binding"]=bindcode;
                            other["columns"]=[`,"binding": "${other["binding"]}"`]
                            other["inputs"]=[`,"Ext": "${other["binding"]}"`]
                            other["props"]=[`,"Ext": "${other["binding"]}"`]
                            other["quicks"]=[`,"Ext": "${other["binding"]}"`,` "Source": "${other["binding"]}","TextField": "name", "ValueField": "value"`]
                        }else if(last_type=="d"){
                            showType="datetime";
                            other["fmt"]="yyyyMMdd"
                            other["inputs"]=[`,"Ext": "${other["fmt"]}"`]
                            other["props"]=[`,"Ext": "${other["fmt"]}"`]
                            other["quicks"]=[`,"Ext": "{Format:'${other["fmt"]}'}"`]

                            // 
                        }
                      
                        // 保存字段配置
                        retO["oOne"][sn]={sn,dataType,nm,width,showType,other};

                        var templateCols=`{ "field": "${sn}","title":"${nm}","width":"${width}", "halign": "center" ${other["columns"].join(",")} }`;
                        var templateInputs=` { "Field": "${sn}", "Name": "${nm}", "ShowType":"${showType}" ${other["inputs"].join(",")} } `
                        var templateProps=`{ "Field":"${sn}", "Name" : "${nm}", "ShowType":"${showType}","DataType": "${dataType}" ,"FilterEnabled": true,"OrderEnabled": true ${other["props"].join(",")}  }`;
                        retO.columns.push(JSON.parse(templateCols))

                        // 
                        one_templateInputs=JSON.parse(templateInputs)
                      
                     
                        retO.inputs.push(one_templateInputs)
                        retO.props.push(JSON.parse(templateProps))
                    })
                    // 添加算法列
                    if(retO.foreignCols){
                        $.each(retO.foreignCols.split("\n"),function(ai,av){
                            
                            var a_foreignCol=av.split(",");
                            if(a_foreignCol.length>0&& a_foreignCol[0] ){
                                // 重新查询
                                if(a_foreignCol[0]=="Out"){
                                    sn=a_foreignCol[1];
                                    nm=a_foreignCol[2];
                                    s_key=a_foreignCol[3];
                                    width="100"
                                    templateCols=`{ "field": "${sn}","title":"${nm}","width":"${width}", "halign": "center", "align": "center"}`;
                                    o_foreignCol=JSON.parse(templateCols)
                                    o_foreignCol["formatter"]= function (V, R, I) {
                                        sn=a_foreignCol[1];
                                        nm=a_foreignCol[2];
                                        s_key=a_foreignCol[3];
                                        is_all=a_foreignCol[4];
                                        if(!V&&!is_all){
                                            return ""
                                        }
                                        return "<a onclick=showDialogList("+I+",'"+sn+"','"+s_key+"')>"+nm+"</a>" }
                                    retO.columns.push(o_foreignCol)
                                }

                                if(a_foreignCol[0]=="Chart"){
                                    sn=a_foreignCol[1]||"onechart";
                                    nm=a_foreignCol[2];
                                    s_key=a_foreignCol[3];
                                    width="100"
                                    templateCols=`{ "field": "${sn}","title":"${nm}","width":"${width}", "halign": "center", "align": "center"}`;
                                    o_foreignCol=JSON.parse(templateCols)
                                    o_foreignCol["formatter"]= function (V, R, I) {
                                        sn=a_foreignCol[1];
                                        nm=a_foreignCol[2];
                                        s_key=a_foreignCol[3];
                                        is_all=a_foreignCol[4];
                                        if(!V&&!is_all){
                                            return ""
                                        }
                                        return "<a onclick=showDialogChart("+I+",'"+sn+"','"+s_key+"')>"+nm+"</a>" }
                                    retO.columns.push(o_foreignCol)
                                }


                            }
                         
                        })
                    }
// 排序
                    if(json.rows[0].orders){
                        let ordersStr=json.rows[0].orders;
                        aOrdersStr=ordersStr.split(",")
                        aOrdersStr.forEach(element => {
                            // true 逆序
                            let sn=element.split(":")[0]||""
                            let sort_by=element.split(":").length>1?(element.split(":")[1]==1?false:true):false
                            var templateOrder=`
                            { "Field": "${sn}", "Type": ${sort_by} }
                           `
                           retO.orders.push(JSON.parse(templateOrder))
                        });
                       
                    };
                    // 查询条件
                    if(json.rows[0].quicks){
                        let quicksStr=json.rows[0].quicks;
                        aQuicksStr=quicksStr.split("\n")
                        aQuicksStr.forEach(element => {
                            let sn=element.split(",")[0]||"";
                            let default_value=element.split(",")[1]||"";
                            
                           if(retO["oOne"][sn]){
                               let nm=retO["oOne"][sn].nm;
                               let width=retO["oOne"][sn].width;
                               let dataType=retO["oOne"][sn].dataType;
                               let showType=retO["oOne"][sn].showType;
                               let type=(showType=="combo"?"QCombox":(showType=="datetime"?"QDatetime":"QText"));
                               
                               let other=retO["oOne"][sn].other;
                           
                            var templateQuicks=` { "Field": "${sn}", "Label": "${nm}",  "Type": "${type}", "Width": ${width}, "Value": "${default_value}" ${other["quicks"].join(",")} } `;
                           
                            
                            retO.quicks.push(JSON.parse(templateQuicks))
                           
                           }
                           
                        });
                       
                    }





            }
        }

    })


      //  input 处理分行new

      let default_rowspan=3;
      inputs=Array.from(retO.inputs);
      let oneRow=[]
      let oneRowTextarea=[];
      $.each(inputs,function(inputsi,inputsv){

        if(oneRow.length==0 &&oneRowTextarea.length>0){
            $.each(oneRowTextarea,function(textareasi,textareasv){
                retO.inputsRet.push(textareasv)
            })
            oneRowTextarea=[]
        }

        if(inputsv.ShowType=="textarea"){
            inputsv["ColSpan"]=default_rowspan;
            oneRowTextarea.push([inputsv]);
            return true;
        }
        oneRow.push(inputsv);
        if(( oneRow.length>0&&oneRow.length%default_rowspan==0)){
            retO.inputsRet.push(oneRow)
            oneRow=[]
        } 
      })
      if(oneRow.length>0){
        retO.inputsRet.push(oneRow)
      }
      if(oneRowTextarea.length>0){
        $.each(oneRowTextarea,function(textareasi,textareasv){
            retO.inputsRet.push(textareasv)
        })
       
    }

    
      return retO
}