; (function(jQuery) {
    jQuery.extend(jQuery.CRUD, {
        Service : function(Options, CView) {
            var CRUD = this;
            var Records = [];
            var paramStr=""
            if(Options.paramStr){
                paramStr="?"+Options.paramStr
            }
            var S = {
                Core : CRUD,
                Base : Options.Base || "",
                Path : Options.Path || "",
                Target : Options.Target,
                GetView : function(Arguments, Callback) {
                  	//添加非Ajax加载界面
                  	if(typeof(CView) != "undefined"){
                  		return Callback(CView);
                  	}
                    jQuery.ajax({
                        type : "POST",
                        data : JSON.stringify({
                            path : S.Path,
                            target : S.Target
                        }),
                        url : S.Base + S.Path + S.Target + "/view.json"+paramStr,
                        contentType : "application/json",
                        dataType : "json",
                        success : function(json) {
                          Callback(json.Response);
                        },
                        error : function(ex) {
                        }
                    });
                },
                Insert : function(Record, Callback) {
                    var Pars = { record : Record };
                    if(jQuery.isArray(Record))
                    {
                        Pars = { records : Record };
                    }
                    jQuery.ajax({
                        type : "POST",
                        data : JSON.stringify(Pars),
                        url : S.Base + S.Path + S.Target + "/insert.json"+paramStr,
                        contentType : "application/json",
                        dataType : "json",
                        success : function(json) {
                            Callback(json);
                        },
                        error : function(ex) {
                        }
                    });
                },
                Update : function(Record, Callback) {
                    jQuery.ajax({
                        type : "POST",
                        data : JSON.stringify({
                            record : Record
                        }),
                        url : S.Base + S.Path + S.Target + "/update.json"+paramStr,
                        contentType : "application/json",
                        dataType : "json",
                        success : function(json) {
                            Callback(json);
                        },
                        error : function(ex) {
                        }
                    });
                },
                Delete : function(Record, Callback) {
                    jQuery.ajax({
                        type : "POST",
                        data : JSON.stringify({
                            record : Record
                        }),
                        url : S.Base + S.Path + S.Target + "/delete.json"+paramStr,
                        contentType : "application/json",
                        dataType : "json",
                        success : function(json) {
                            Callback(json);
                        },
                        error : function(ex) {
                        }
                    });
                },
                Query : function(Arguments, Callback) {
                    jQuery.ajax({
                        type : "POST",
                        data : JSON.stringify({
                            conditions : Arguments.Filters,
                            order : Arguments.Orders,
                            size : Arguments.Size,
                            index : Arguments.Index
                        }),
                        url : S.Base + S.Path + S.Target + "/query.json"+paramStr,
                        contentType : "application/json",
                        dataType : "json",
                        success : function(json) {
                            Callback(json);
                        },
                        error : function(ex) {
                        }
                    });
                },
		        GetFooter: Options.GetFooter || null
            };

            return S;
        }
    });
})(jQuery); 