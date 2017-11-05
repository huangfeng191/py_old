jQuery.extend(
{
    Filter: function (Container, Options)
    {
        jQuery.ImplantStyle("Filter", (Options.Skin || "Default"));

        var Cmp = jQuery(Container).data("component");

        var CreateOperate = function (Container, Field, Value)
        {
            Container.html("<input />");
            var Source = [];
            if (Field)
            {
                if (Field.Operates)
                {
                    Source = Field.Operates;
                }
                else if (Field.ShowType == "combo" || Field.ShowType == "combotree")
                {
                    Source =
                    [
                        { Value: "=", Name: "等于" },
                        { Value: "!=", Name: "不等于" },
                        { Value: "nil", Name: "不存在" }
                    ];
                    if (Field.DataType == "String")
                    {
                        Source.push({ Value: "blank", Name: "为空" });
                    }
                }
                else
                {
                    switch (Field.DataType)
                    {
                        case "String":
                            {
                                Source =
						        [
                                    { Value: "like", Name: "包含" },
							        { Value: "=", Name: "等于" },
                                    { Value: "!=", Name: "不等于" },
                                    { Value: "nil", Name: "不存在" },
                                    { Value: "blank", Name: "为空" }
						        ];
                            }
                            break;
                        case "DateTime":
                            {
                                Source =
						        [
							        { Value: "=", Name: "等于" },
                                    { Value: "!=", Name: "不等于" },
							        { Value: ">", Name: "大于" },
							        { Value: "<", Name: "小于" },
							        { Value: ">=", Name: "大于等于" },
							        { Value: "<=", Name: "小于等于" },
                                    { Value: "nil", Name: "不存在" }
						        ];
                            }
                            break;
                        case "Number":
                            {
                                Source =
						        [
							        { Value: "=", Name: "等于" },
                                    { Value: "!=", Name: "不等于" },
							        { Value: ">", Name: "大于" },
							        { Value: "<", Name: "小于" },
							        { Value: ">=", Name: "大于等于" },
							        { Value: "<=", Name: "小于等于" },
                                    { Value: "nil", Name: "不存在" }
						        ];
                            }
                            break;
                    }
                }
            }
            var Input = Container.find("input").combobox({ width: 70, panelHeight: 168, valueField: 'Value', textField: 'Name', data: Source, editable: false });
            Container.parents("div.filter").data("GetOperate", function () { return Input.combobox("getValue"); });

            if (Value)
            {
                var In = false;
                for (var i = 0, len = Source.length; i < len; i++)
                {
                    if (Source[i].Value == Value)
                    {
                        In = true;
                        break;
                    }
                }
                if (In)
                {
                    Input.combobox("setValue", Value);
                }
                else if (Source.length > 0)
                {
                    Input.combobox("setValue", Source[0].Value);
                }
            }
        };
        //生成值
        var CreateValue = function (Container, Field, Value)
        {
            if (Field)
            {
                Container.html("<input/>");
                switch (Field.ShowType)
                {
                    case "datetime":
                        {
                            var Input = Container.html("<input type=\"text\" class='date yyyyMMddHHmmss' onclick=\"new WdatePicker({skin:'default',readOnly:true,isShowToday:false,dateFmt:'" + Field.Ext + "'})\" >").find("input");
                            Container.parents("div.filter").data("GetValue", function ()
                            {
                                var V = Input.val();
                                if (V.length > 0)
                                {
                                    if (Field.DataType == "Number")
                                    {
                                        V = ConvertToDate(V, Field.Ext).getTime() / 1000;
                                    }
                                    return V;
                                }
                                else
                                {
                                    return null;
                                }
                            });
                            if (Value != undefined && Value != null)
                            {
                                if (Field.DataType == "Number")
                                {
                                    Value = new Date(Value * 1000).FormatString(Field.Ext);
                                }
                                Input.val(Value);
                            }
                        }
                        break;
                    case "combo":
                        {
                            var Input = Container.find("input").combobox({ width: 156, panelHeight: 168, valueField: 'value', textField: 'name', data: Cmp.Sources[Field.Ext], editable: false });
                            Container.parents("div.filter").data("GetValue", function ()
                            {
                                var V = Input.combobox("getValue");
                                if (Field.DataType == "Number")
                                {
                                    if (jQuery.isNumeric(V))
                                    {
                                        return Number(V);
                                    }
                                    else
                                    {
                                        return null;
                                    }
                                }
                                else
                                {
                                    if (V.length > 0)
                                    {
                                        return V;
                                    }
                                    else
                                    {
                                        return null;
                                    }
                                }
                            });
                            if (Value != undefined && Value != null)
                            {
                                Input.combobox("setValue", Value);
                            }
                            else if (Cmp.Sources[Field.Ext].length > 0)
                            {
                                Input.combobox("setValue", Cmp.Sources[Field.Ext][0].Id);
                            }
                        }
                        break;
                    case "combotree":
                        {
                            var Input = Container.find("input").combotree({ width: 156, lines: true, data: Cmp.Sources[Field.Ext], editable: false });
                            Container.parents("div.filter").data("GetValue", function ()
                            {
                                var V = Input.combotree("getValue");
                                if (Field.DataType == "Number")
                                {
                                    if (jQuery.isNumeric(V))
                                    {
                                        return Number(V);
                                    }
                                    else
                                    {
                                        return null;
                                    }
                                }
                                else
                                {
                                    if (V.length > 0)
                                    {
                                        return V;
                                    }
                                    else
                                    {
                                        return null;
                                    }
                                }
                            });
                            if (Value != undefined && Value != null)
                            {
                                Input.combotree("setValue", Value);
                            }
                            else if (Cmp.Sources[Field.Ext].length > 0)
                            {
                                Input.combotree("setValue", Cmp.Sources[Field.Ext][0].Id);
                            }
                        }
                        break;
                    case "text":
                    default:
                        {
                            var Input = Container.find("input").validatebox();
                            if (Field.DataType == "Number")
                            {
                                Input.keyup(function (Evt)
                                {
                                    if (/^-?[0-9]+\.?[0-9]*$/.test(Input.val()) == false)
                                    {
                                        Input.val(Input.val().substr(0, Input.val().length - 1));
                                    }
                                });
                            }
                            Container.parents("div.filter").data("GetValue", function ()
                            {
                                var V = Input.val();
                                if (Field.DataType == "Number")
                                {
                                    if (jQuery.isNumeric(V))
                                    {
                                        return Number(V);
                                    }
                                    else
                                    {
                                        return null;
                                    }
                                }
                                else
                                {
                                    if (V.length > 0)
                                    {
                                        return V;
                                    }
                                    else
                                    {
                                        return null;
                                    }
                                }
                            });
                            if (Value != undefined && Value != null)
                            {
                                Input.val(Value);
                            }
                        }
                        break;
                }
            }
        };

        //字段切换事件
        var FieldChange = function (Field)
        {
            var Filter = jQuery(this).parents(".filter");

            CreateOperate(Filter.find("span[col=operate]"), Field, "=");

            CreateValue(Filter.find("span[col=value]"), Field);
        };

        var CreateFilter = function (Filter)
        {
            jQuery(Cmp.Template).appendTo(List).find("span").each(function (i, ele)
            {
                ele = jQuery(ele);
                switch (ele.attr("col"))
                {
                    case "number":
                        {
                            ele.html(List.find("div").length);
                        }
                        break;
                    case "field":
                        {
                            var Input = ele.find("input").combobox({ panelHeight: 168, valueField: 'Field', textField: 'Name', data: Cmp.Fields, editable: false, onSelect: FieldChange });
                            if (Filter)
                            {
                                Input.combobox("setValue", Filter.Field);
                            }
                            else if (Cmp.Fields.length > 0)
                            {
                                Input.combobox("setValue", Cmp.Fields[0].Field);
                            }
                            ele.parents("div.filter").data("GetField", function () { return Input.combobox("getValue"); });
                        }
                        break;
                    case "operate":
                        {
                            var Field = Cmp.Fields[0];
                            if (Filter)
                            {
                                Field = Cmp.Field[Filter.Field];
                            }
                            CreateOperate(ele, Field, (Filter ? Filter.Operate : "="));
                        }
                        break;
                    case "value":
                        {
                            CreateValue(ele, Cmp.Field[(Filter ? Filter.Field : Cmp.Fields[0].Field)], (Filter ? Filter.Value : null));
                        }
                        break;
                    case "relation":
                        {
                            var Input = ele.find("input").combobox({ panelHeight: 168, valueField: 'Value', textField: 'Name', data: [{ Value: "and", Name: "并且" }, { Value: "or", Name: "或者"}], editable: false });
                            ele.parents("div.filter").data("GetRelation", function () { return Input.combobox("getValue"); });
                            if (Filter)
                            {
                                Input.combobox("setValue", Filter.Relation);
                            }
                            else
                            {
                                Input.combobox("setValue", "and");
                            }
                        }
                        break;
                    case "delete":
                        {
                            ele.click(function (Evt)
                            {
                                jQuery(this).parents("div.filter").remove();
                                List.find("div.filter>span[col=number]").each(function (i, ele)
                                {
                                    jQuery(ele).html(i + 1);
                                });
                            });
                        }
                        break;
                }
            });
        };

        if (!Cmp)
        {
            Cmp =
			{
			    Container: jQuery(Container),
			    Options: Options,
			    Filters: (Options.Filters ? Options.Filters : []),
			    Field: {}, //字段索引
			    Fields: Options.Fields,
			    Sources: {},
			    Template: jQuery.GetTemplate(function ()
			    {
			        /*
			        <div class="filter">
			        <span class="width30" col="number"></span>

			        <span class="width80" col="field" ><input style="width:95px;"/></span>

			        <span class="width70" col="operate"><input style="width:70px;"/></span>

			        <span class="width140" col="value" ><input style="width:154px;"/></span>

			        <span class="width50" col="relation"><input style="width:50px;"/></span>

			        <span class="delete width30" col="delete">删除</span>
			        </div>
			        */
			    }),
			    //获取条件列表并返回
			    Get: function ()
			    {
			        var Filters = [];
			        for (var i = 0, Arr = this.Filters, len = Arr.length; i < len; i++)
			        {
			            if (!Cmp.Field[Arr[i].Field])
			            {
			                Filters.push(Arr[i]);
			            }
			        }

			        for (var i = 0, Arr = this.Container.find("div.content>div.filter"), len = Arr.length; i < len; i++)
			        {
			            var Filter = jQuery(Arr[i]);
			            if (Filter.data("GetValue")() != null || Filter.data("GetOperate")() == "nil" || Filter.data("GetOperate")() == "blank")
			            {
			                Filters.push(
						    {
						        Field: Filter.data("GetField")(),
						        Operate: Filter.data("GetOperate")() == "blank" ? "=" : Filter.data("GetOperate")(),
						        Relation: Filter.data("GetRelation")(),
						        Value: Filter.data("GetOperate")() == "blank" || Filter.data("GetOperate")() == "nil" ? "" : Filter.data("GetValue")(),
						        DataType: Cmp.Field[Filter.data("GetField")()].DataType,
						        From: "filter"
						    });
			            }
			        }
			        return Filters
			    }
			};
            Cmp.Container.addClass("filter_framework");

            //生成字段索引
            for (var i = 0, Arr = Cmp.Fields, len = Arr.length, All = Cmp.Field; i < len; i++)
            {
                All[Arr[i].Field] = Arr[i];
            }

            //生成绑定数据源
            if (Options.Bindings && Options.Bindings.length > 0)
            {
                for (var i = 0, Arr = Options.Bindings, len = Arr.length, All = Cmp.Sources; i < len; i++)
                {
                    All[Arr[i].Code] = Arr[i].Records;
                }
            }

            //初始化，生成表头，空条件列表和新增按钮
            jQuery(jQuery.GetTemplate(function ()
            {
                /*
                <div class="title">
                <span class="width30">序号</span>
                <span class="width80">字段</span>
                <span class="width70">操作符</span>
                <span class="width140">数值</span>
                <span class="width50">关系</span>
                <span class="width30">操作</span>
                </div>
                <div class="content">
				
                </div>
                <div class="search_box">
                <a href="#" class="btn btn_common right" style="margin-right:20px"><span class="icons icon_add"></span>增加条件</a>
                </div>
                */
            })).appendTo(Container).find("a").click(function (Evt) { CreateFilter(); });
            var List = Cmp.Container.find("div.content");

            //判断是否有有效过滤条件
            var Has = false;
            for (var i = 0, Arr = Cmp.Filters, len = Arr.length; i < len; i++)
            {
                if (Cmp.Field[Arr[i].Field])
                {
                    Has = true;
                }
            }

            if (Has)
            {
                //有初始条件，生成初始条件,绑定删除按钮事件
                for (var i = 0, Arr = Cmp.Filters, len = Arr.length; i < len; i++)
                {
                    if (Arr[i].Operate == "=" && Arr[i].Value == "")
                    {
                        Arr[i].Operate = "blank";
                    }
                    if (Cmp.Field[Arr[i].Field])
                    {
                        CreateFilter(Arr[i]);
                    }
                }
            }
            else if (Options.ShowAll != false)
            {
                for (var i = 0, Arr = Cmp.Fields, len = Arr.length; i < len; i++)
                {
                    CreateFilter({ Field: Arr[i].Field, Operate: (Arr[i].Operate || "="), Relation: "and" });
                }
            }
            else
            {
                //默认生成第一行
                CreateFilter();
            }

            //设置条件列表容器最大高度
            List.css("max-height", Cmp.Container.height() - 66);

            jQuery(Container).data("component", Cmp);
        }
        return Cmp;
    }
});

