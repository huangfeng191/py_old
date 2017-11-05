//(function(jQuery)
//{
jQuery.extend(jQuery.CRUD,
	{
	    View: function (Options)
	    {
	        var Loading = jQuery.Loading({ Message: "文件上传中……", Timeout: 600 });
	        if (!jQuery(document).data("template"))
	        {
	            jQuery(document).data("template", true);

	            //Top
	            jQuery.ImplantTemplate("crud_temp_top", jQuery.GetTemplate(function ()
	            {
	                /*
	                <table class="top_container"><tr>

	                <td class="left_container">
	                {{if Title}}
	                <div class="title"><nobr>{{Title}}</nobr></div>
	                {{/if}}

	                {{ if Quicks && Quicks.length > 0 }}
	                {{each Quicks as Q i}}
	                <span></span>
	                {{/each}}

	                <button command="query" class="icon icon_query" type="button">
	                查询
	                </button>
	                {{ /if }}
	                {{ if Advance }}
	                <button command="advance" class="icon icon_object_manage" type="button">
	                高级查询对象管理
	                </button>
	                {{ /if }}
	                </td>

	                <td class="right_container">
	                {{each Buttons as btn i}}
	                {{if btn.Command}}
	                <button command="{{btn.Command}}" title="{{btn.Tooltip}}" style="display:none;" class="{{if btn.Name.length > 0}}icon{{else}}iconly{{/if}} icon_{{btn.Command}}" type="button">
	                {{if btn.Name.length > 0}}{{btn.Name}}{{else}}&nbsp;{{/if}}
	                </button>
	                {{else}}
	                <span class="line">&nbsp;</span>
	                {{/if}}
	                {{/each}}
	                </td>

	                </tr></table>
	                */
	            }));

	            //Form
	            jQuery.ImplantTemplate("crud_temp_form", jQuery.GetTemplate(function ()
	            {
	                /*
	                {{each Form as Group g}}
	                <div group="{{Group.Code}}" class="group">
	                {{if Form.length > 1}}<div class="title"><span>{{Group.Title}}</span></div>{{/if}}
	                <table style="{{Group.Style}}">

	                {{each Group.Inputs as Row r}}
	                <tr>

	                {{each Row as Cell c}}
	                {{if Cell.Field}}
	                <td class="label" field_label="{{Cell.Field}}" rowspan="{{Cell.RowSpan}}" colspan="1">{{Cell.Name}}</td>
	                <td class="content" field_input={{Cell.Field}} rowspan="{{Cell.RowSpan}}" colspan="{{Cell.ColSpan * 2 - 1}}">
	                <div class='wrap'>
	                {{if Cell.ShowType == "textarea"}}<textarea
	                {{else}}<input {{/if}}
	                class="{{if Cell.ShowType == "datetime"}}Wdate {{else if Cell.ShowType == "upload" || Cell.ShowType == "uploadpic" || Cell.ShowType == "gispos" || Cell.ShowType == "gisarea" }}text_button {{else if Cell.ShowType == "text"}}easyui-validatebox {{/if}}default {{if Cell.Class}}{{ Cell.Class}}{{/if}}"
	                field="{{Cell.Field}}" valuetype="{{Cell.DataType}}" showtype="{{Cell.ShowType}}"
	                type="{{if Cell.ShowType == "password"}}password{{else if Cell.ShowType == "combocheck"}}combo{{else if Cell.ShowType == "checkbox"}}checkbox{{else}}text{{/if}}"
	                {{if Cell.Validate && Cell.Validate.length > 0}} validator="{{Cell.Validate}}"
	                {{else if Cell.ShowType == "datetime" && Cell.DataType == "Number"}} validator="{Valids:{regexp:['为必填项','^([0-9]+(.[0-9]+)?){{if !Cell.Required}}?{{/if}}$']},Message:'{{Cell.Name}}'}"
	                {{else if Cell.DataType == "Number"}} validator="{Valids:{regexp:['必须为数值','^[\\-\\+]?([0-9]+(\\.[0-9]+)?){{if !Cell.Required}}?{{/if}}$']},Message:'{{Cell.Name}}'}"
	                {{else if Cell.DataType == "Phone"}} validator="{Valids:{regexp:['必须为有效的电话号码','^((?:0?(13|15|17|18|14)[0-9][0-9]{8})|(?:([0-9]{3,4}\-)?[0-9]{6,8})){{if !Cell.Required}}?{{/if}}$']},Message:'{{Cell.Name}}'}"
	                {{else if Cell.DataType == "IP"}} validator="{Valids:{regexp:['必须为有效IP地址','^((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){{if !Cell.Required}}?{{/if}}$']},Message:'{{Cell.Name}}'}"
	                {{else if Cell.DataType == "EMail"}} validator="{Valids:{regexp:['必须为有效的邮箱地址','^([\\w-]+@[\\w-]+\\.(com|net|org|edu|mil|tv|biz|info)){{if !Cell.Required}}?{{/if}}$']},Message:'{{Cell.Name}}'}"
	                {{else if Cell.Required}} validator="{Valids:{regexp:['为必填项','\\S+']},Message:'{{Cell.Name}}'}"
	                {{/if}}

	                {{if Cell.MaxLength}} maxlength="{{Cell.MaxLength}}" {{/if}}

	                {{if Cell.ShowType == "combo" || Cell.ShowType == "combocheck" || Cell.ShowType == "combotree"}} source="{{Cell.Ext}}"
	                {{else if Cell.ShowType == "datetime"}} onclick="new WdatePicker({skin:'default',readOnly:{{if Cell.ReadOnly === false}} false {{else}} true{{/if}},isShowToday:false,dateFmt:'{{Cell.Ext}}'})" format="{{Cell.Ext}}"
	                {{else if Cell.ShowType == "textarea"}} style="resize:none;{{Cell.Ext}}"
	                {{else if Cell.ShowType == "text"}} style="{{Cell.Ext}}"{{/if}}

	                {{if Cell.Required}} require="require"{{/if}}

	                {{if Cell.Editable === false}} editable="editable"{{/if}}
	            
	                {{if Cell.ShowType == "textarea"}} ></textarea>
	                {{else if Cell.ShowType == "upload"}} exts="{{Cell.Ext}}"{{if Cell.HasContent == true}} hascontent="true"{{/if}} readonly="readonly" /><button type="button" cmd="upload" class="upload"{{if Cell.HasContent == true}} hascontent="true"{{/if}}>...</button>
	                {{else if Cell.ShowType == "uploadpic"}} exts="{{Cell.Ext || "gif|bmp|jpg|jpeg|png"}}"{{if Cell.HasContent == true}} hascontent="true"{{/if}} readonly="readonly" /><button type="button" cmd="upload" class="upload"{{if Cell.HasContent == true}} hascontent="true"{{/if}}>...</button>
	                {{else if Cell.ShowType == "gispos"}} exts="{{Cell.Ext}}" readonly="readonly" /><button type="button" cmd="gispos" class="gispos">...</button>
	                {{else if Cell.ShowType == "gisarea"}} exts="{{Cell.Ext}}" readonly="readonly" /><button type="button" cmd="gisarea" class="gisarea">...</button>
	                {{else}} />{{/if}}
	                <div class='border border-with-{{Cell.ShowType}}'>
	                {{if Cell.Unit}}<span class="unit">{{Cell.Unit}}</span>{{/if}}
	                {{if Cell.Required && Cell.ShowType != 'combo' && Cell.ShowType != 'combotree' && Cell.ShowType != 'checkbox'}}<span class="required">*</span>{{/if}}
	                </div>
	                </div>
	                </td>
	                {{else}}
	                <td class="label blank" rowspan="{{Cell.RowSpan}}" colspan="1">{{Cell.Name}}</td>
	                <td class="content blank" rowspan="{{Cell.RowSpan}}" colspan="{{Cell.ColSpan * 2 - 1}}"></td>
	                {{/if}}
	                {{/each}}

	                </tr>
	                {{/each}}
	                {{if Group.Blank}}
	                <tr style="height:{{Group.Blank}}px"><td></td></tr>
	                {{/if}}
	                </table></div>
	                {{/each}}
	                */
	            }));
	        }

	        var CRUD = this;

	        var ContentHeight, GridHeight, FormHeight;

	        var Template_TB = template.compile(jQuery.GetTemplate(function ()
	        {
	            /*
	            {{include "crud_temp_top"}}

	            <div class="content_container">

	            <div class="grid_container"><table></table></div>

	            {{if FormContent && FormContent.length > 0 || Form && Form.length > 0}}
	            <div class="separator_bar">
	            <div class='min' state="min"></div>
	            <div class='normal' state="normal"></div>
	            <div class='max' state="max"></div>
	            </div>

	            <div class="form_container">
	            <div class="group_container">
	            {{if FormContent && FormContent.length > 0}}
	            {{FormContent}}
	            {{else}}

	            {{include "crud_temp_form"}}

	            {{/if}}
	            </div>
	            <div class="button_container">
	            <button command="confirm" class="confirm disabled" type="button">确定</button>
	            <button command="cancel"class="disabled" type="button" >取消</button>
	            </div>
	            </div>
	            {{/if}}
	            </div>
	            
	            <div class="custom_container"></div>
	            */
	        }), { escape: false });

	        var Template_LR = template.compile(jQuery.GetTemplate(function ()
	        {
	            /*
	            {{include "crud_temp_top"}}

	            <div class="content_container">
	            
	            <div class="grid_container"><table></table></div>
	            
	            {{if FormContent && FormContent.length > 0 || Form && Form.length > 0}}
	            <div class="separator_bar">
	            <div class='min' state="min"></div>
	            <div class='normal' state="normal"></div>
	            <div class='max' state="max"></div>
	            </div>

	            <div class="form_container">
	            <div class="group_container">
	            {{if FormContent && FormContent.length > 0}}
	            {{FormContent}}
	            {{else}}

	            {{include "crud_temp_form"}}

	            {{/if}}
	            </div>
	            <div class="button_container">
	            <button command="confirm" class="confirm disabled" type="button">确定</button>
	            <button command="cancel"class="disabled" type="button" >取消</button>
	            </div>
	            </div>
	            {{/if}}
	            </div>
	            */
	        }), { escape: false });

	        var Template_POP = template.compile(jQuery.GetTemplate(function ()
	        {
	            /*
	            {{include "crud_temp_top"}}

	            <div class="grid_container"><table></table></div>
	            <div class="custom_container"></div>
	            */
	        }), { escape: false });

	        var Buttons =
            {
                Buttons:
                [
                    { Command: "reset", Name: "", Tooltip: "复位" },
                    { Command: "filter", Name: "", Tooltip: "过滤" },
                    { Command: "order", Name: "", Tooltip: "排序" },
                    { Command: "column", Name: "", Tooltip: "列定义" }
                ]
            };

	        function MouseUp(Evt)
	        {
	            if (V.Container.find(">.content_container>.separator_bar").hasClass("selected"))
	            {
	                if (V.Object.Layout == "LR")
	                {
	                    var Offset = Evt.pageX - V.Container.find(">.content_container>.separator_bar").removeClass("selected").data("pos");
	                    var Gh = GridHeight + Offset;
	                    var Fh = FormHeight - Offset;
	                    if (Gh >= Options.Grid.MinHeight && Fh >= 0)
	                    {
	                        GridHeight = Gh;
	                        V.LSD.FormSize = FormHeight = Fh;
	                        HD.LocalStorage.Set(V.LSK, { FormSize: FormHeight }, 7 * 24 * 3600);
	                        V.Form.Resize();
	                    }
	                }
	                else
	                {
	                    var Offset = Evt.pageY - V.Container.find(">.content_container>.separator_bar").removeClass("selected").data("pos");
	                    var Gh = GridHeight + Offset;
	                    var Fh = FormHeight - Offset;
	                    if (Gh >= Options.Grid.MinHeight && Fh >= 0)
	                    {
	                        GridHeight = Gh;
	                        V.LSD.FormSize = FormHeight = Fh;
	                        HD.LocalStorage.Set(V.LSK, { FormSize: FormHeight }, 7 * 24 * 3600);
	                        V.Form.Resize();
	                    }
	                }

	                jQuery("div.seperator_line").remove();
	            }
	        };
	        function MouseDown(Evt)
	        {
	            if (jQuery(Evt.target).hasClass("separator_bar"))
	            {
	                if (V.Object.Layout == "LR")
	                {
	                    jQuery(this).addClass("selected").data("pos", Evt.pageX);
	                    jQuery("<div class='seperator_line vertical'></div>").appendTo(V.Container.find(">.content_container"))
			                .css("left", Evt.pageX - 30).mousemove(MouseMove).height(V.Container.find(">.content_container").height());
	                }
	                else
	                {
	                    jQuery(this).addClass("selected").data("pos", Evt.pageY);
	                    jQuery("<div class='seperator_line'></div>").appendTo(V.Container.find(">.content_container"))
			                .css("top", Evt.pageY - V.TopContainer.outerHeight(true) - 30).mousemove(MouseMove);
	                }
	            }
	        };
	        function MouseMove(Evt)
	        {
	            if (V.Object.Layout == "LR")
	            {
	                if (Evt.pageX >= Options.Grid.MinHeight)
	                {
	                    jQuery(this).css("left", Evt.pageX - 30);
	                }
	            }
	            else
	            {
	                if (Evt.pageY >= V.TopContainer.outerHeight(true) + Options.Grid.MinHeight)
	                {
	                    jQuery(this).css("top", Evt.pageY - V.TopContainer.outerHeight(true) - 30);
	                }
	            }
	        };

	        var Button_All = {};

	        var FilterPropertys = [];
	        var Filters = [];

	        var OrderPropertys = [];
	        var Orders = [];

	        var ColumnPropertys = [];

	        var UniquePropertys = null

	        function FilterClear(Fields)
	        {
	            if (jQuery.isArray(Fields))
	            {
	                var All = {};
	                for (var i = 0, len = Fields.length; i < len; i++)
	                {
	                    All[Fields[i]] = Fields[i];
	                }
	                Filters = [].concat(Filters);
	                for (var i = Filters.length - 1; i >= 0; i--)
	                {
	                    if (All[Filters[i].Field])
	                    {
	                        Filters.splice(i, 1);
	                    }
	                }
	            }
	            else
	            {
	                Filters = [];
	            }
	            Filters.Merge = FilterMerge;
	            Filters.Clear = FilterClear;
	        };

	        function FilterMerge(Items)
	        {
	            var All = {};
	            for (var i = 0, len = Items.length; i < len; i++)
	            {
	                All[Items[i].Field + "_" + Items[i].Operate] = Items[i];
	            }
	            Filters = [].concat(Filters);
	            for (var i = 0, len = Filters.length; i < len; i++)
	            {
	                if (All[Filters[i].Field + "_" + Filters[i].Operate])
	                {
	                    if (All[Filters[i].Field + "_" + Filters[i].Operate].Replaceable)
	                    {
	                        delete All[Filters[i].Field + "_" + Filters[i].Operate];
	                    }
	                    else
	                    {
	                        Filters.splice(i, 1, All[Filters[i].Field + "_" + Filters[i].Operate]);
	                        delete All[Filters[i].Field + "_" + Filters[i].Operate];
	                    }
	                }
	            }
	            for (var Key in All)
	            {
	                Filters.push(All[Key]);
	            }
	            Filters.Merge = FilterMerge;
	            Filters.Clear = FilterClear;
	        };

	        function OrderClear(Fields)
	        {
	            if (jQuery.isArray(Fields))
	            {
	                var All = {};
	                for (var i = 0, len = Fields.length; i < len; i++)
	                {
	                    All[Fields[i]] = Fields[i];
	                }
	                Orders = [].concat(Orders);
	                for (var i = Orders.length - 1; i >= 0; i--)
	                {
	                    if (All[Orders[i].Field])
	                    {
	                        Orders.splice(i, 1);
	                    }
	                }
	            }
	            else
	            {
	                Orders = [];
	            }
	            Orders.Merge = OrderMerge;
	            Orders.Clear = OrderClear;
	        };

	        function OrderMerge(Items)
	        {
	            var All = {};
	            for (var i = 0, len = Items.length; i < len; i++)
	            {
	                All[Items[i].Field] = Items[i];
	            }
	            Orders = [].concat(Orders);
	            for (var i = 0, len = Orders.length; i < len; i++)
	            {
	                if (All[Orders[i].Field])
	                {
	                    if (All[Orders[i].Field].Replaceable)
	                    {
	                        delete All[Orders[i].Field];
	                    }
	                    else
	                    {
	                        Orders.splice(i, 1, All[Orders[i].Field]);
	                        delete All[Orders[i].Field];
	                    }
	                }
	            }
	            for (var Key in All)
	            {
	                Orders.push(All[Key]);
	            }
	            Orders.Merge = OrderMerge;
	            Orders.Clear = OrderClear;
	        };

	        var FieldRegexp = new RegExp("\\.|\\[|\\]\\.");

	        function GetField(Object, Field)
	        {
	            if (FieldRegexp.test(Field))
	            {
	                var F = Field.split(FieldRegexp)[0];
	                var Cur = Object[F];
	                if (Cur)
	                {
	                    return GetField(Cur, Field.replace(new RegExp("^" + F + "(\\.|\\[|\\]\\.)"), ""));
	                }
	                else
	                {
	                    return null;
	                }
	            }
	            else
	            {
	                return Object[Field];
	            }
	        }

	        function SetField(Object, Field, Value)
	        {
	            if (FieldRegexp.test(Field))
	            {
	                var F = Field.split(FieldRegexp)[0];
	                Field = Field.replace(new RegExp("^" + F), "");
	                var Cur = Object[F];
	                if (!Cur)
	                {
	                    if (Field.charAt(0) == "[")
	                    {
	                        Cur = Object[F] = [];
	                    }
	                    else
	                    {
	                        Cur = Object[F] = {};
	                    }
	                }
	                SetField(Cur, Field.replace(/^(\.|\[|\]\.)/, ""), Value);
	            }
	            else
	            {
	                Object[Field] = Value;
	            }
	        }

	        //统一绑定下拉框数据源
	        function BindComboBoxes(Sources, Container)
	        {
	            for (var i = 0, len = Sources.length; i < len; i++)
	            {
	                Container.find("[source=" + Sources[i].Code + "]").addClass("combox-complete").each(function (idx, ele)
	                {
	                    Combo = jQuery(ele);
	                    var Type = Combo.attr("showtype");
	                    var Items = jQuery.extend(true, [], Sources[i].Records);
	                    if (Type == "combocheck")
	                    {
	                        Combo.combobox({
	                            valueField: 'value',
	                            textField: 'name',
	                            data: Items,
	                            editable: false,
	                            multiple: true,
	                            height: 26,
	                            width: 154,
	                            formatter: function (Row) { return "<div class='combocheckbox'>" + Row.name + "</div>"; }
	                        });
	                    }
	                    else if (Type == "combotree")
	                    {
	                        Combo.combotree({
	                            lines: true,
	                            height: 26,
	                            data: Items
	                        });
	                    }
	                    else
	                    {
	                        if (Combo.attr("require") != "require")
	                        {
	                            Items.unshift({ name: "[未设置]", value: (Combo.attr("datatype") == "Number" ? 0 : "") });
	                        }
	                        Combo.combobox({ valueField: 'value', textField: 'name', data: Items, editable: false, height: 26 });
	                    }
	                });
	            }

	            Container.find("[source]").each(function (i, ele)
	            {
	                if (!$(this).hasClass("combox-complete"))
	                {
	                    $(this).combobox({ valueField: 'value', textField: 'name', data: [], editable: false, height: 26 });
	                    //V.ShowMessage("缺少代码为“" + jQuery(ele).attr("source") + "”的绑定数据源");
	                }
	            });
	        };

	        //验证器
	        var Validators =
			{
			    Result: [],
			    Method:
				{
				    length: function (Message, Min, Max)
				    {
				        if (typeof (Min) === "number" && typeof (Max) === "number" && (this.length < Min || this.length > Max))
				        {
				            Validators.Result.push("<span style='color:red;'>" + Message + "</span>长度必须在" + Min + "至" + Max + "之间");
				            return false;
				        }
				        else if (typeof (Min) === "number" && this.length < Min)
				        {
				            Validators.Result.push("<span style='color:red;'>" + Message + "</span>长度不能小于" + Min);
				            return false;
				        }
				        else if (typeof (Max) === "number" && this.length > Max)
				        {
				            Validators.Result.push("<span style='color:red;'>" + Message + "</span>长度不能大于" + Max);
				            return false;
				        }
				        else
				        {
				            return true;
				        }
				    },
				    range: function (Message, Min, Max)
				    {
				        if (this.length > 0 && !isNaN(Number(this)))
				        {
				            var N = Number(this);
				            if (typeof (Min) === "number" && typeof (Max) === "number" && (N < Min || N > Max))
				            {
				                Validators.Result.push("<span style='color:red;'>" + Message + "</span>数值必须在" + Min + "至" + Max + "之间");
				                return false;
				            }
				            else if (typeof (Min) === "number" && N < Min)
				            {
				                Validators.Result.push("<span style='color:red;'>" + Message + "</span>数值不能小于" + Min);
				                return false;
				            }
				            else if (typeof (Max) === "number" && N > Max)
				            {
				                Validators.Result.push("<span style='color:red;'>" + Message + "</span>数值不能大于" + Max);
				                return false;
				            }
				            else
				            {
				                return true;
				            }
				        }
				        else if (this.length > 0)
				        {
				            Validators.Result.push("<span style='color:red;'>" + Message + "</span>不是有效的数值格式");
				            return false;
				        }
				        else
				        {
				            return true;
				        }
				    },
				    digits: function (Message, Digits)
				    {
				        if (this.length > 0 && !isNaN(Number(this)) && this.indexOf(".") != -1 && this.length - this.indexOf(".") - 1 > Digits)
				        {
				            Validators.Result.push("<span style='color:red;'>" + Message + "</span>小数位数不能大于" + Digits);
				            return false;
				        }
				        else
				        {
				            return true;
				        }
				    },
				    regexp: function (Message, MessageExt, Exp)
				    {
				        var Regx = new RegExp(Exp);
				        if (!Regx.test(this))
				        {
				            Validators.Result.push("<span style='color:red;'>" + Message + "</span>" + MessageExt);
				            return false;
				        }
				        else
				        {
				            return true;
				        }
				    }
				}
			};

	        function Validate(Group, Callback)
	        {
	            var Filter = Group.shift();
	            CRUD.Service.Query({ Filters: Filter.Filters, Orders: [], Size: 1, Index: 1 }, function (Result)
	            {
	                if (Result.Code == 0)
	                {
	                    if (Result.Response.total > 0)
	                    {
	                        V.ShowMessage(Filter.Message.join("_") + "不能重复");
	                        Callback(false);
	                    }
	                    else
	                    {
	                        if (Group.length == 0)
	                        {
	                            Callback(true);
	                        }
	                        else
	                        {
	                            Validate(Group, Callback);
	                        }
	                    }
	                }
	                else
	                {
	                    V.ShowMessage(Result.Message);
	                    Callback(false);
	                }
	            });
	        }

	        var V =
			{
			    Context: window,
			    Core: CRUD,
			    BindingDefaults: Options.BindingDefaults || null,
			    Container: null,
			    Object: null,
			    Property: {},
			    Grid:
				{
				    Options:
                    {
                        pagination: true,
                        pageSize: 20,
                        displayMsg: "",
                        singleSelect: true,
                        rownumbers: true,
                        loadMsg: '',
                        loader: function (Params, Success, Error)
                        {
                            if (CRUD.FirstQuery)
                            {
                                CRUD.FirstQuery = false;
                                V.QuickFilter({}, function (Result) { });
                                CRUD.QueryEnabled = true;
                            }

                            if (CRUD.QueryEnabled)
                            {
                                var State = true;
                                if (CRUD.Behavior.BeforeQuery)
                                {
                                	
                                    Filters.Merge = FilterMerge;
                                    Filters.Clear = FilterClear;
                                    Orders.Merge = OrderMerge;
                                    Orders.Clear = OrderClear;
                                    State = CRUD.Behavior.BeforeQuery(Filters, Orders, Params.rows, Params.page);
                                }
                               
                                if (State === true)
                                {
                                    var Pars =
							        {
							            Filters: Filters,
							            Orders: Orders,
							            Size: Params.rows || 999999,
							            Index: Params.page || 0
							        };

                                    //保存localstorage
                                    //HD.LocalStorage.Set(V.LSK, V.GetSettings(), 7 * 24 * 3600);

                                    if (Orders.length > 0)
                                    {
                                        CRUD.View.Button.Highlight("order");
                                    }
                                    else
                                    {
                                        CRUD.View.Button.Normal("order");
                                    }

                                    CRUD.Service.Query(Pars, function (Result)
                                    {
                                        if (Result.Code == 0)
                                        {
                                            var State = true;
                                            V.Button.Normal(["insert", "upsert", "update", "delete"]);
                                            V.Button.Disable(["update", "delete", "confirm", "cancel"]);
                                            V.Button.Enable(["insert", "upsert"]);
                                            if (V.Object.Layout != "POP")
                                            {
                                                V.Form.Clear();
                                                V.Form.Disable();
                                            }
                                            if (CRUD.Behavior.AfterQuery)
                                            {
                                                State = CRUD.Behavior.AfterQuery(Result.Response);
                                            }
                                            if (State)
                                            {
                                                if (jQuery.isFunction(CRUD.Service.GetFooter))
                                                {
                                                    Result.Response.footer = CRUD.Service.GetFooter(Result.Response.rows);
                                                }
                                                Success(Result.Response);
                                                if (V.Grid.AfterLoad)
                                                {
                                                    V.Grid.AfterLoad();
                                                }
                                                if (V.Form.Auto)
                                                {
                                                    V.Form.Resize(V.Form.Auto.Query);
                                                }
                                            }
                                        }
                                        else
                                        {
                                            V.ShowMessage(Result.Message);
                                        }
                                    });
                                }
                                else if (State === false)
                                {
                                    V.Grid.Clear();
                                }
                            }
                            else
                            {
                                CRUD.QueryEnabled = true;
                            }
                        },
                        onClickRow: function (Index, Row)
                        {
                            V.Grid.CurrentIndex = Index;
                            V.Grid.CurrentRow = Row;

                            CRUD.Behavior.Grid.RowClick(Row, Index);
                        },
                        onDblClickRow: function (Index, Row)
                        {
                            CRUD.Behavior.Grid.RowDblClick(Row);
                        }
                    },
				    CurrentRow: null,
				    CurrentIndex: null,
				    Query: function ()
				    {
				        V.Grid.Element.datagrid("load");
				        if (V.Object.Layout != "POP")
				        {
				            V.Form.Clear();
				        }
				        this.CurrentIndex = null;
				        this.CurrentRow = null;
				    },
				    Refresh: function ()
				    {
				        V.Grid.Element.datagrid("reload");
				        if (V.Object.Layout != "POP")
				        {
				            V.Form.Clear();
				        }
				        this.CurrentIndex = null;
				        this.CurrentRow = null;
				    },
				    InsertRow: function (Row, Index)
				    {
				        V.Grid.Element.datagrid("insertRow", { index: Index, row: Row });
				    },
				    UpdateRow: function (Row)
				    {
				        V.Grid.Element.datagrid("updateRow", { index: this.CurrentIndex, row: Row });
				    },
				    Export: function ()
				    {
				        //var FileName = (V.Object.ExportName || "导出记录") + new Date().FormatString("yyyy-MM-dd");
				        var FileName = "导出记录";
				        if (jQuery.isFunction(V.Object.ExportName))
				        {
				            FileName = V.Object.ExportName();
				        }
				        else if (V.Object.ExportName)
				        {
				            FileName = V.Object.ExportName;
				        } else
				        {
				            FileName = top.mh.History.Current.Item.Name;
				        }
				        var _title = FileName;
				        FileName += new Date().FormatString("yyyy-MM-dd");

				        var State = true;
				        if (CRUD.Behavior.BeforeQuery)
				        {
				            Filters.Merge = FilterMerge;
				            Filters.Clear = FilterClear;
				            Orders.Merge = OrderMerge;
				            Orders.Clear = OrderClear;
				            State = CRUD.Behavior.BeforeQuery(Filters, Orders);
				        }
				        if (State)
				        {
				            var Pars =
                            {
                                Filters: Filters,
                                Orders: Orders,
                                Size: 999999,
                                Index: 1
                            };
				            CRUD.Service.Query(Pars, function (Result)
				            {
				                var State = true;

				                if (CRUD.Behavior.AfterQuery)
				                {
				                    State = CRUD.Behavior.AfterQuery(Result);
				                }

				                if (State)
				                {

				                    Loading.Show();
				                    function GetRowValue(row, field)
				                    {
				                        try
				                        {
				                            return eval("row['" + field.replace(/\./g, "']['") + "']");
				                        }
				                        catch (e)
				                        {
				                            return "";
				                        }
				                    }

				                    //生成数据记录
				                    var Content = ["<table style='font-family: 宋体;font-size:16px;'>"];

				                    //生成表头
				                    var Fields = [];
				                    for (var i = 0, All = V.Column, Arr = V.Grid.Element.datagrid("getColumnFields", true), len = Arr.length; i < len; i++)
				                    {
				                        if (All[Arr[i]] && All[Arr[i]].hidden != true)
				                        {
				                            Fields.push(Arr[i]);
				                        }
				                    }
				                    for (var i = 0, All = V.Column, Arr = V.Grid.Element.datagrid("getColumnFields", false), len = Arr.length; i < len; i++)
				                    {
				                        if (All[Arr[i]] && All[Arr[i]].hidden != true)
				                        {
				                            Fields.push(Arr[i]);
				                        }
				                    }

				                    var Field = {};
				                    var Align = {};
				                    for (var i = 0, Arr = (V.Object.Properties || V.Object.Propertys), len = Arr.length; i < len; i++)
				                    {
				                        Field[Arr[i].Field] = Arr[i].DataType;
				                        Align[Arr[i].Field] = Arr[i].align || "center";
				                    }

				                    var Records = [];
				                    var HideFields = {};
				                    if (Result.Response.total > 0)
				                    {
				                        Records = Result.Response.rows;
				                        if (CRUD.Behavior.BeforeExport)
				                        {
				                            var Hfs = CRUD.Behavior.BeforeExport(Records, Content, Fields);
				                            if (jQuery.isArray(Hfs))
				                            {
				                                for (var i = 0, len = Hfs.length; i < len; i++)
				                                {
				                                    HideFields[Hfs[i]] = true;
				                                }
				                            }
				                        }
				                    }

				                    Content.push("<tr><td style=\"font-size: 16px; text-align: center; height: 32px; padding: 4px;border:solid 0.5pt #000000;\" colspan=\"" + Fields.length + "\">" + _title + "</td></tr>");

				                    var DataColumns = {};
				                    var Opts = V.Grid.Element.datagrid("options");
				                    for (var i = 0, FR = Opts.frozenColumns, R = Opts.columns, len = FR.length > R.length ? FR.length : R.length; i < len; i++)
				                    {
				                        Content.push("<tr>");
				                        //锁定列
				                        if (i < FR.length)
				                        {
				                            for (var j = 0, Cells = FR[i], lenj = Cells.length; j < lenj; j++)
				                            {
				                                if (!Cells[j].hidden && !HideFields[Cells[j].field] && Cells[j].checkbox != true)
				                                {
				                                    //Fields.push(Cells[j].field);
				                                    Content.push("<td style=\"border:solid 0.5pt #000000;\" rowspan=\"");
				                                    Content.push(Cells[j].rowspan);
				                                    Content.push("\" colspan=\"");
				                                    Content.push(Cells[j].colspan);
				                                    Content.push("\" >&nbsp;");
				                                    Content.push(Cells[j].title);
				                                    Content.push("</td>");

				                                    if (Cells[j]["datatype"] && Cells[j]["datatype"] == "number")
				                                    {
				                                        DataColumns[Cells[j]["field"]] = Cells[j];
				                                    }
				                                }
				                            }
				                        }
				                        //非锁定列
				                        if (i < R.length)
				                        {
				                            for (var j = 0, Cells = R[i], lenj = Cells.length; j < lenj; j++)
				                            {
				                                if (!Cells[j].hidden && !HideFields[Cells[j].field] && Cells[j].checkbox != true)
				                                {
				                                    //Fields.push(Cells[j].field);
				                                    Content.push("<td style=\"border:solid 0.5pt #000000;\" rowspan=\"");
				                                    Content.push(Cells[j].rowspan);
				                                    Content.push("\" colspan=\"");
				                                    Content.push(Cells[j].colspan);
				                                    Content.push("\" >&nbsp;");
				                                    Content.push(Cells[j].title);
				                                    Content.push("</td>");

				                                    if (Cells[j]["datatype"] && Cells[j]["datatype"] == "number")
				                                    {
				                                        DataColumns[Cells[j]["field"]] = Cells[j];
				                                    }
				                                }
				                            }
				                        }

				                        Content.push("</tr>");
				                    }


				                    for (var i = 0, Rows = Records, len = Rows.length; i < len; i++)
				                    {
				                        Content.push("<tr>");
				                        for (var j = 0, lenj = Fields.length; j < lenj; j++)
				                        {
				                            if (!HideFields[Fields[j]])
				                            {
				                                var cell_formatter = V.Column[Fields[j]].formatter || null;
				                                var cell_val = GetRowValue(Rows[i], Fields[j]);
				                                if (!cell_val && String(cell_val) != "0") { cell_val = ""; }
				                                var cell_type = Field[Fields[j]] || "String";
				                                var cell_align = Align[Fields[j]] || "center";
				                                 if (V.Object.ExportFmt&&Field[Fields[j]] == 'String'){
                                                     Content.push("<td style=\"border:solid 0.5pt #000000;mso-number-format:'\@';\"");
                                                    } else if(/^[0-9]*$/.test(cell_val) && Field[Fields[j]] == 'String') {
				                                	Content.push("<td style=\"border:solid 0.5pt #000000;mso-number-format:'\@';\"");
	                                            }else{
	                                            	Content.push("<td style=\"border:solid 0.5pt #000000;\"");      
	                                            	
	                                            }                                                                 

				                                
				                                
				                                Content.push(" align='" + cell_align + "'");
				                                if (Fields[j].datatype != 'Number')
				                                {
				                                    if (cell_val)
				                                    {
				                                        if (cell_val.length == 1)
				                                        {
				                                            if (cell_val != '0')
				                                            {
				                                                Content.push("vnd.ms-excel.numberformat:@\"");
				                                            }
				                                        } else
				                                        {
				                                             if ((!((!isNaN(cell_val)) && (cell_val + "  ").substring(0, 1) != '0' && (cell_val + "  ").substring(0, 2) != '0.'))&&(!V.Object.ExportFmt)) {
                                                                    if (cell_val && jQuery.isFunction(cell_val.substr) && (cell_val + "  ").trim().substr(0, 1) == '0') {
                                                                        cell_val = "&nbsp;" + cell_val + "";
                                                                    } else if ((cell_val + "").indexOf("-") >= 0) {
                                                                        cell_val = "&nbsp;" + cell_val + "";
                                                                    }
				                                            }


				                                        }
				                                    } else
				                                    {
				                                        Content.push("vnd.ms-excel.numberformat:@\"");
				                                    }
				                                }
				                                Content.push(">");

				                                if (cell_formatter)
				                                {
				                                    if (typeof (cell_formatter) == "string")
				                                    {
				                                        cell_formatter = eval(cell_formatter);
				                                    }
				                                    try { cell_val = cell_formatter(cell_val, Rows[i], i); } catch (e) { }
				                                }

				                                Content.push(cell_val);
				                                Content.push("</td>");
				                                // Content.push("<td style=\"border:solid 0.5pt #000000;\"");
				                                // if (V.Column[Fields[j]].formatter)
				                                // {
				                                //     if (Field[Fields[j]] == "Number"
				                                // 		|| (DataColumns[Fields[j]] && DataColumns[Fields[j]]["datatype"] && DataColumns[Fields[j]]["datatype"] == "number"))
				                                //     {
				                                //         Content.push(">&nbsp;"); //Content.push(" x:num >"); 20160115 by yucq number类型的时间导出格式问题
				                                //         Content.push(V.Column[Fields[j]].formatter(GetRowValue(Rows[i], Fields[j]), Rows[i], i));
				                                //     }
				                                //     else
				                                //     {
				                                //         Content.push(">&nbsp;");
				                                //         Content.push(V.Column[Fields[j]].formatter(GetRowValue(Rows[i], Fields[j]), Rows[i], i));
				                                //     }
				                                // }
				                                // else if (Field[Fields[j]] == "Number")
				                                // {
				                                //     Content.push(" x:num >");
				                                //     Content.push(GetRowValue(Rows[i], Fields[j]));
				                                // }
				                                // else
				                                // {
				                                //     if (DataColumns[Fields[j]] && DataColumns[Fields[j]]["datatype"] && DataColumns[Fields[j]]["datatype"] == "number")
				                                //     {
				                                //         Content.push(" x:num >");
				                                //         Content.push(GetRowValue(Rows[i], Fields[j]));
				                                //     }
				                                //     else
				                                //     {
				                                //         Content.push(">&nbsp;");
				                                //         Content.push(GetRowValue(Rows[i], Fields[j]));
				                                //     }
				                                // }
				                                // Content.push("</td>");
				                            }
				                        }
				                        Content.push("</tr>");
				                    }
									 if (V.Object.ExportFoot == true ? true : false) {
										if (Fields.length > 1)
										{
											var cs0 = Math.floor(Fields.length / 2);
											var cs1 = Fields.length - cs0;
											Content.push("<tr><td style=\"border:solid 0.5pt #000000;\" colspan='")
											Content.push(cs0);
											Content.push("' >值班人:");
											//Content.push(top.GCtx.user.nm);
											Content.push("</td><td style='border:solid 0.5pt #000000;text-align: right;' colspan='")
											Content.push(cs1);
											Content.push("' >日期:");
											Content.push(new Date().FormatString("yyyy-MM-dd"));
											Content.push("</td></tr>");
										}
										else
										{
											Content.push("<tr><td style=\"border:solid 0.5pt #000000;\">值班人:");
											//Content.push(top.GCtx.user.nm);
											Content.push(" 日期:");
											Content.push(new Date().FormatString("yyyy-MM-dd"));
											Content.push("</td></tr>");
										}
                                    }
				                    Content.push("</table>");

				                    var ConHtml = Content.join("");
				                    var strXlsName = FileName + ".xls";
				                    var tempForm = $('<form action="/export" method="post"></form>');
				                    var exportContent = $('<input type="hidden" id="exportContent" name="exportContent" />');
				                    var fileName = $('<input type="hidden" id="FileName" name="FileName" />');
				                    exportContent.val(ConHtml);
				                    tempForm.append(exportContent);
				                    fileName.val(strXlsName);
				                    tempForm.append(fileName);
				                    document.body.appendChild(tempForm[0]);
				                    Loading.Hide();
				                    tempForm.submit();
				                    document.body.removeChild(tempForm[0]);
				                }
				            });
				        }
				    },
				    Clear: function ()
				    {
				        V.Grid.Element.datagrid("loadData", []);
				        this.CurrentIndex = null;
				        this.CurrentRow = null;
				        Filters = [];
				        Orders = [];
				        V.Form.Clear();
				        V.Form.Disable();
				    }
				},
			    Button:
				{
				    //按钮是否可用
				    Enabled: function (Which)
				    {
				        return !Button_All[Which].hasClass("disabled");
				    },
				    //禁用按钮
				    Disable: function (Which)
				    {
				        var Arr = V.Object.Buttons || [];
				        if (jQuery.isArray(Which))
				        {
				            Arr = Which;
				        }
				        if (jQuery.type(Which) == "string")
				        {
				            Arr = [Which];
				        }
				        for (var i = 0, len = Arr.length; i < len; i++)
				        {
				            if (Button_All[Arr[i]])
				            {
				                Button_All[Arr[i]].addClass("disabled");
				            }
				        }
				    },
				    //启用按钮
				    Enable: function (Which)
				    {
				        var Arr = V.Object.Buttons || [];
				        if (jQuery.isArray(Which))
				        {
				            Arr = Which;
				        }
				        if (jQuery.type(Which) == "string")
				        {
				            Arr = [Which];
				        }
				        for (var i = 0, len = Arr.length; i < len; i++)
				        {
				            if (Button_All[Arr[i]])
				            {
				                Button_All[Arr[i]].removeClass("disabled");
				            }
				        }
				    },
				    //高亮显示
				    Highlight: function (Which)
				    {
				        var Arr = [];
				        if (jQuery.isArray(Which))
				        {
				            Arr = Which;
				        }
				        if (jQuery.type(Which) == "string")
				        {
				            Arr = [Which];
				        }
				        for (var i = 0, len = Arr.length; i < len; i++)
				        {
				            if (Button_All[Arr[i]])
				            {
				                Button_All[Arr[i]].addClass("selected");
				            }
				        }
				    },
				    //普通显示
				    Normal: function (Which)
				    {
				        var Arr = [];
				        if (jQuery.isArray(Which))
				        {
				            Arr = Which;
				        }
				        if (jQuery.type(Which) == "string")
				        {
				            Arr = [Which];
				        }
				        for (var i = 0, len = Arr.length; i < len; i++)
				        {
				            if (Button_All[Arr[i]])
				            {
				                Button_All[Arr[i]].removeClass("selected");
				            }
				        }
				    },
				    //显示按钮
				    Show: function (Which)
				    {
				        var Arr = [];
				        if (jQuery.isArray(Which))
				        {
				            Arr = Which;
				        }
				        if (jQuery.type(Which) == "string")
				        {
				            Arr = [Which];
				        }
				        for (var i = 0, len = Arr.length; i < len; i++)
				        {
				            if (Button_All[Arr[i]])
				            {
				                Button_All[Arr[i]].show();
				            }
				        }
				    },
				    //隐藏按钮
				    Hide: function (Which)
				    {
				        var Arr = [];
				        if (jQuery.isArray(Which))
				        {
				            Arr = Which;
				        }
				        if (jQuery.type(Which) == "string")
				        {
				            Arr = [Which];
				        }
				        for (var i = 0, len = Arr.length; i < len; i++)
				        {
				            if (Button_All[Arr[i]])
				            {
				                Button_All[Arr[i]].hide();
				            }
				        }
				    },
				    //模拟点击
				    Click: function (Which)
				    {
				        var Arr = [];
				        if (jQuery.isArray(Which))
				        {
				            Arr = Which;
				        }
				        if (jQuery.type(Which) == "string")
				        {
				            Arr = [Which];
				        }
				        for (var i = 0, len = Arr.length; i < len; i++)
				        {
				            if (Button_All[Arr[i]])
				            {
				                Button_All[Arr[i]].trigger("click");
				            }
				        }
				    }
				},
			    Form:
                {
                    Clear: function (Fields)
                    {
                        if (V.Form.BeforeClear)
                        {
                            V.Form.BeforeClear(Fields);
                        }

                        if (Fields)
                        {
                            Fields = "(" + Fields.join(")(") + ")";
                            for (var i = 0, Eles = V.FormContainer.find(">div.group_container>div.group [field]"), len = Eles.length; i < len; i++)
                            {
                                var Ele = jQuery(Eles[i]);
                                var Field = Ele.attr("field");
                                if (Fields.indexOf("(" + Field + ")") > -1)
                                {
                                    var Type = Ele.attr("showtype");
                                    if (Type == "upload")
                                    {
                                        Ele.removeData("content");
                                    }
                                    switch (Type)
                                    {
                                        case "combo":
                                            {
                                                var Items = Ele.combobox("getData");
                                                if (Items.length > 0)
                                                {
                                                    if (V.BindingDefaults && V.BindingDefaults[Ele.attr("source")])
                                                    {
                                                        Ele.combobox("setValue", V.BindingDefaults[Ele.attr("source")]);
                                                    }
                                                    else
                                                    {
                                                        Ele.combobox("setValue", Items[0].value);
                                                    }
                                                }
                                                else
                                                {
                                                    Ele.combobox("clear");
                                                }
                                            }
                                            break;
                                        case "combocheck":
                                            {
                                                var Items = Ele.combobox("getData");
                                                if (Items.length > 0)
                                                {
                                                    if (V.BindingDefaults && V.BindingDefaults[Ele.attr("source")])
                                                    {
                                                        Ele.combobox("setValues", V.BindingDefaults[Ele.attr("source")]);
                                                    }
                                                    else
                                                    {
                                                        Ele.combobox("setValues", [Items[0].value]);
                                                    }
                                                }
                                                else
                                                {
                                                    Ele.combobox("clear");
                                                }
                                            }
                                            break;
                                        case "combotree":
                                            {
                                                Ele.combotree("clear");
                                            }
                                            break;
                                        case "datetime":
                                            {
                                                Ele.val("");
                                            }
                                            break;
                                        case "checkbox":
                                            {
                                                //Ele.removeProp("checked");
                                                Ele[0].checked = false;
                                            }
                                            break;
                                        default:
                                            {
                                                Ele.val("");
                                            }
                                            break;
                                    }
                                }
                            }
                        }
                        else
                        {
                            //不指定字段，全部清空
                            for (var i = 0, Eles = V.FormContainer.find(">div.group_container>div.group [field]"), len = Eles.length; i < len; i++)
                            {
                                var Ele = jQuery(Eles[i]);
                                var Field = Ele.attr("field");
                                var Type = Ele.attr("showtype");
                                switch (Type)
                                {
                                    case "combo":
                                        {
                                            var Items = Ele.combobox("getData");
                                            if (Items.length > 0)
                                            {
                                                if (V.BindingDefaults && V.BindingDefaults[Ele.attr("source")])
                                                {
                                                    Ele.combobox("setValue", V.BindingDefaults[Ele.attr("source")]);
                                                }
                                                else
                                                {
                                                    Ele.combobox("setValue", Items[0].value);
                                                }
                                            }
                                            else
                                            {
                                                Ele.combobox("clear");
                                            }
                                        }
                                        break;
                                    case "combocheck":
                                        {
                                            var Items = Ele.combobox("getData");
                                            if (Items.length > 0)
                                            {
                                                if (V.BindingDefaults && V.BindingDefaults[Ele.attr("source")])
                                                {
                                                    Ele.combobox("setValues", V.BindingDefaults[Ele.attr("source")]);
                                                }
                                                else
                                                {
                                                    Ele.combobox("setValues", [Items[0].value]);
                                                }
                                            }
                                            else
                                            {
                                                Ele.combobox("clear");
                                            }
                                        }
                                        break;
                                    case "combotree":
                                        {
                                            Ele.combotree("clear");
                                        }
                                        break;
                                    case "datetime":
                                        {
                                            Ele.val("");
                                        }
                                        break;
                                    case "checkbox":
                                        {
                                            //Ele.removeProp("checked");
                                            Ele[0].checked = false;
                                        }
                                        break;
                                    default:
                                        {
                                            Ele.val("");
                                        }
                                        break;
                                }
                            }
                        }

                        V.FormContainer.find(".sign_red").removeClass("sign_red");
                        V.FormContainer.find(".sign_yellow").removeClass("sign_yellow");

                        if (V.Form.AfterClear)
                        {
                            V.Form.AfterClear();
                        }
                    },
                    Enable: function (Fields)
                    {
                        if (V.Form.BeforeEnable)
                        {
                            V.Form.BeforeEnable(Fields);
                        }

                        if (Fields)
                        {
                            Fields = "(" + Fields.join(")(") + ")";
                            for (var i = 0, Eles = V.FormContainer.find(">div.group_container>div.group [field]"), len = Eles.length; i < len; i++)
                            {
                                var Ele = jQuery(Eles[i]);
                                var Field = Ele.attr("field");
                                if (Ele.attr("editable") != "editable" && Fields.indexOf("(" + Field + ")") > -1)
                                {
                                    var Type = Ele.attr("showtype");
                                    switch (Type)
                                    {
                                        case "combo":
                                        case "combocheck":
                                            {
                                                Ele.combobox("enable");
                                            }
                                            break;
                                        case "combotree":
                                            {
                                                Ele.combotree("enable");
                                            }
                                            break;
                                        case "datetime":
                                            {
                                                Ele.removeAttr("disabled");
                                            }
                                            break;
                                        default:
                                            {
                                                Ele.removeAttr("disabled");
                                            }
                                            break;
                                    }
                                }
                            }
                        }
                        else
                        {
                            //不指定字段，全部清空
                            for (var i = 0, Eles = V.FormContainer.find(">div.group_container>div.group [field]"), len = Eles.length; i < len; i++)
                            {
                                var Ele = jQuery(Eles[i]);
                                var Field = Ele.attr("field");
                                var Type = Ele.attr("showtype");
                                if (Ele.attr("editable") != "editable")
                                {
                                    switch (Type)
                                    {
                                        case "combo":
                                        case "combocheck":
                                            {
                                                Ele.combobox("enable");
                                            }
                                            break;
                                        case "combotree":
                                            {
                                                Ele.combotree("enable");
                                            }
                                            break;
                                        case "datetime":
                                            {
                                                Ele.removeAttr("disabled");
                                            }
                                            break;
                                        default:
                                            {
                                                Ele.removeAttr("disabled");
                                            }
                                            break;
                                    }
                                }
                            }
                        }

                        V.FormContainer.find("button.upload").removeClass("disabled");

                        V.GridContainer.removeClass("grid_active");
                        V.FormContainer.addClass("form_active");

                        if (V.Form.AfterEnable)
                        {
                            V.Form.AfterEnable();
                        }
                    },
                    Disable: function (Fields)
                    {
                        if (V.Form.BeforeDisable)
                        {
                            V.Form.BeforeDisable(Fields);
                        }

                        if (Fields)
                        {
                            Fields = "(" + Fields.join(")(") + ")";
                            for (var i = 0, Eles = V.FormContainer.find(">div.group_container>div.group [field]"), len = Eles.length; i < len; i++)
                            {
                                var Ele = jQuery(Eles[i]);
                                var Field = Ele.attr("field");
                                if (Fields.indexOf("(" + Field + ")") > -1)
                                {
                                    var Type = Ele.attr("showtype");
                                    switch (Type)
                                    {
                                        case "combo":
                                        case "combocheck":
                                            {
                                                Ele.combobox("disable");
                                            }
                                            break;
                                        case "combotree":
                                            {
                                                Ele.combotree("disable");
                                            }
                                            break;
                                        case "datetime":
                                            {
                                                Ele.attr("disabled", "disabled");
                                            }
                                            break;
                                        default:
                                            {
                                                Ele.attr("disabled", "disabled");
                                            }
                                            break;
                                    }
                                }
                            }
                        }
                        else
                        {
                            //不指定字段，全部清空
                            for (var i = 0, Eles = V.FormContainer.find(">div.group_container>div.group [field]"), len = Eles.length; i < len; i++)
                            {
                                var Ele = jQuery(Eles[i]);
                                var Field = Ele.attr("field");
                                var Type = Ele.attr("showtype");
                                switch (Type)
                                {
                                    case "combo":
                                    case "combocheck":
                                        {
                                            Ele.combobox("disable");
                                        }
                                        break;
                                    case "combotree":
                                        {
                                            Ele.combotree("disable");
                                        }
                                        break;
                                    case "datetime":
                                        {
                                            Ele.attr("disabled", "disabled");
                                        }
                                        break;
                                    default:
                                        {
                                            Ele.attr("disabled", "disabled");
                                        }
                                        break;
                                }
                            }
                        }

                        V.FormContainer.find("button.upload").addClass("disabled");

                        V.GridContainer.addClass("grid_active");
                        V.FormContainer.removeClass("form_active");

                        if (V.Form.AfterDisable)
                        {
                            V.Form.AfterDisable();
                        }
                    },
                    Get: function (IsUpdate)
                    {
                        //初始化验证结果
                        Validators.Result = [];

                        var Record = (IsUpdate ? { _id: V.Grid.CurrentRow._id} : {}); //modify by fox 2015-06-10 仅保存Form中的字段，

                        if (V.Form.BeforeGet)
                        {
                            V.Form.BeforeGet(Record, !IsUpdate, Validators.Result);
                        }

                        var Valid = null;
                        //modify by xjw 2015-08-20 Form中的datagrid中的field不保存
                        for (var i = 0, Eles = V.FormContainer.find(">div.group_container>div.group [field]:not(.datagrid-view [field])"), len = Eles.length; i < len; i++)
                        {
                            var Ele = jQuery(Eles[i]);
                            var Field = Ele.attr("field");
                            var Type = Ele.attr("showtype");
                            var ValueType = Ele.attr("valuetype");
                            if (Ele.attr("hidden") != "hidden" && Ele.attr("validator"))
                            {
                                Valid = eval('(' + Ele.attr("validator") + ')');
                            }
                            else
                            {
                                Valid = null;
                            }

                            var Value = null;
                            switch (Type)
                            {
                                case "combo":
                                    {
                                        Value = Ele.combobox("getValue");
                                    }
                                    break;
                                case "combocheck":
                                    {
                                        Value = Ele.combobox("getValues");
                                        //字段为数组，取消验证
                                        Valid = null;
                                    }
                                    break;
                                case "combotree":
                                    {
                                        Value = Ele.combotree("getValue");
                                    }
                                    break;
                                case "datetime":
                                    {
                                        Value = Ele.val();
                                        if (ValueType == "Number" && Value.length > 0)
                                        {
                                            Value = "" + (ConvertToDate(Value, Ele.attr("format")).getTime() / 1000);
                                        }
                                    }
                                    break;
                                case "checkbox":
                                    {
                                        //Value = Ele.prop("checked") ? "1" : "0";
                                        Value = Ele[0].checked ? "1" : "0";
                                    }
                                    break;
                                default:
                                    {
                                        Value = Ele.val();
                                    }
                                    break;
                            }

                            //执行验证逻辑
                            if (Valid)
                            {
                                var Valids = Valid.Valids;
                                for (var Key in Valids)
                                {
                                    var Vld = Valids[Key];
                                    Vld.unshift(Valid.Message);
                                    if (Validators.Method[Key].apply(Value, Vld))
                                    {
                                        //验证通过，移除标红和标黄
                                        Ele.removeClass("sign_red").removeClass("sign_yellow");
                                    }
                                    else
                                    {
                                        //验证失败，增加标红或标黄
                                        if (Ele.attr("require") === "require")
                                        {
                                            Ele.addClass("sign_red");
                                        }
                                        else
                                        {
                                            Ele.addClass("sign_yellow");
                                        }
                                    }
                                }
                            }

                            //upload with content
                            if (Type == "upload" && Ele.attr("hascontent") == "true")
                            {
                                SetField(Record, Field + "_content", Ele.data("content"));
                            }


                            switch (ValueType)
                            {
                                case "Number":
                                    {
                                        if (jQuery.isArray(Value))
                                        {
                                            var Arr = [];
                                            for (var j = 0, lenj = Value.length; j < lenj; j++)
                                            {
                                                Arr.push(Number(Value[j]));
                                            }
                                            SetField(Record, Field, Arr);
                                        }
                                        else if (jQuery.isNumeric(Value))
                                        {
                                            SetField(Record, Field, Number(Value));
                                        }
                                        else
                                        {
                                            SetField(Record, Field, null);
                                        }
                                    }
                                    break;
                                case "Boolean":
                                    {
                                        if (Value === "false" || Value === "true")
                                        {
                                            SetField(Record, Field, Value);
                                        }
                                        else
                                        {
                                            SetField(Record, Field, null);
                                        }
                                    }
                                    break;
                                case "DateTime":
                                default:
                                    {
                                        SetField(Record, Field, Value);
                                    }
                                    break;
                            }
                        }

                        if (V.Form.AfterGet)
                        {
                            var Records = V.Form.AfterGet(Record, !IsUpdate, Validators.Result);
                            if (Records)
                            {
                                Record = Records;
                            }
                        }

                        return Record;
                    },
                    Set: function (Command)
                    {
                        V.FormContainer.find(".sign_red").removeClass("sign_red");
                        V.FormContainer.find(".sign_yellow").removeClass("sign_yellow");

                        var Record = Command == "insert" ? {} : (V.Grid.CurrentRow || {});
                        if (V.Form.BeforeSet)
                        {
                            V.Form.BeforeSet(Record, ((Command == "insert" || Command == "upsert") ? true : false));
                        }

                        for (var i = 0, Eles = V.FormContainer.find(">div.group_container>div.group [field]"), len = Eles.length; i < len; i++)
                        {
                            var Ele = jQuery(Eles[i]);
                            var Field = Ele.attr("field");
                            var Type = Ele.attr("showtype");
                            var Value = GetField(Record, Field);
                            //if(Record[Field] != undefined && Record[Field] != null)
                            //{
                            //    Value = Record[Field];
                            //}

                            //upload with content
                            if (Type == "upload" && Ele.attr("hascontent") == "true")
                            {
                                Ele.data("content", GetField(Record, Field + "_content"));
                            }

                            switch (Type)
                            {
                                case "combo":
                                    {
                                        if (Value != null)
                                        {
                                            if (Command == "insert")
                                            {
                                                Ele.combobox("setValue", Value);
                                            }
                                            else
                                            {
                                                //判断当前值是否在Items中
                                                var InItems = false;
                                                for (var j = 0, value = Ele.combobox("options").valueField, Items = Ele.combobox("options").data || [], lenj = Items.length; j < lenj; j++)
                                                {
                                                    if (Items[j][value] == Value)
                                                    {
                                                        InItems = true;
                                                        break;
                                                    }
                                                }
                                                if (InItems)
                                                {
                                                    Ele.combobox("setValue", Value);
                                                }
                                                else
                                                {
                                                    Ele.combobox("clear");
                                                }
                                            }
                                        }
                                        else// if(Ele.attr("require") == "require")
                                        {
                                            var Items = Ele.combobox("getData");
                                            if (Items.length > 0)
                                            {
                                                if (V.BindingDefaults && V.BindingDefaults[Ele.attr("source")])
                                                {
                                                    Ele.combobox("setValue", V.BindingDefaults[Ele.attr("source")]);
                                                }
                                                else
                                                {
                                                    Ele.combobox("setValue", Items[0].value);
                                                }
                                            }
                                            else
                                            {
                                                Ele.combobox("clear");
                                            }
                                        }
                                        //                                        else
                                        //                                        {
                                        //                                            Ele.combobox("clear");
                                        //                                        }
                                    }
                                    break;
                                case "combocheck":
                                    {
                                        if (Value != null)
                                        {
                                            if (Command == "insert")
                                            {
                                                Ele.combobox("setValues", Value);
                                            }
                                            else
                                            {
                                                var Va = {};
                                                for (var j = 0, Items = Ele.combobox("options").data || [], lenj = Items.length; j < lenj; j++)
                                                {
                                                    Va[Items[j].value] = Items[j];
                                                }
                                                var Vs = [];
                                                for (var j = 0, lenj = Value.length; j < lenj; j++)
                                                {
                                                    if (Va[Value[j]])
                                                    {
                                                        Vs.push(Value[j]);
                                                    }
                                                }
                                                Ele.combobox("setValues", Vs);
                                            }
                                        }
                                        else if (Ele.attr("require") == "require")
                                        {
                                            var Items = Ele.combobox("getData");
                                            if (Items.length > 0)
                                            {
                                                if (V.BindingDefaults && V.BindingDefaults[Ele.attr("source")])
                                                {
                                                    Ele.combobox("setValues", V.BindingDefaults[Ele.attr("source")]);
                                                }
                                                else
                                                {
                                                    Ele.combobox("setValues", [Items[0].value]);
                                                }
                                            }
                                            else
                                            {
                                                Ele.combobox("clear");
                                            }
                                        }
                                        else
                                        {
                                            Ele.combobox("clear");
                                        }
                                    }
                                    break;
                                case "combotree":
                                    {
                                        Ele.combotree("setValue", Value);
                                    }
                                    break;
                                case "checkbox":
                                    {
                                        if (Value == "1")
                                        {
                                            //Ele.prop("checked", "checked");
                                            Ele[0].checked = true;
                                        }
                                        else
                                        {
                                            //Ele.removeProp("checked");
                                            Ele[0].checked = false;
                                        }
                                    }
                                    break;
                                case "datetime":
                                    {
                                        if (Value != null)
                                        {
                                            if (Ele.attr("valuetype") == "Number")
                                            {
                                                Ele.val(new Date(Value * 1000).FormatString(Ele.attr("format")));
                                            }
                                            else
                                            {
                                                Ele.val(Value);
                                            }
                                        }
                                        else
                                        {
                                            Ele.val("");
                                        }
                                    }
                                    break;
                                default:
                                    {
                                        if (Value != null)
                                        {
                                            Ele.val(Value);
                                        }
                                        else
                                        {
                                            Ele.val("");
                                        }
                                    }
                                    break;
                            }
                        }

                        if (V.Form.AfterSet)
                        {
                            V.Form.AfterSet(Record, ((Command == "insert" || Command == "upsert") ? true : false));
                        }
                    },
                    Validate: function (Record, Callback)
                    {
                        if (Validators.Result.length == 0)
                        {
                            if (UniquePropertys)
                            {
                                var Group = [];
                                for (var Key in UniquePropertys)
                                {
                                    var Msg = [];
                                    var Fs = [{ Field: "_id", Value: Record["_id"], Operate: "!=", Relation: "and"}];
                                    if (Record["__pid"])
                                    {
                                        Fs.push({ Field: "__pid", Value: Record["__pid"], Operate: "=", Relation: "and" });
                                    }
                                    var InFiled = 0, Empty = 0;
                                    for (var i = 0, Arr = UniquePropertys[Key], len = Arr.length; i < len; i++)
                                    {
                                        if (Arr[i].Field in V.Field)
                                        {
                                            InFiled += 1;
                                            if (Record[Arr[i].Field] == "")
                                            {
                                                Empty += 1;
                                            }
                                        }
                                    }
                                    if (InFiled > Empty)//如果所有在表单定义中的字段都为空则调过验证
                                    {
                                        for (var i = 0, Arr = UniquePropertys[Key], len = Arr.length; i < len; i++)
                                        {
                                            var F = { Field: Arr[i].Field, Value: Record[Arr[i].Field], Operate: "=", Relation: "and" };
                                            
                                            if (F.Value == "")// || F.Value == undefined || F.Value == null)
                                            {
                                                F.Operate = "blank";
                                            }

                                            Fs.push(F);
                                            if (Arr[i].Name)
                                            {
                                                Msg.push(Arr[i].Name);
                                            }
                                        }
                                        Group.push({ Message: Msg, Filters: Fs });
                                    }
                                }
                                //验证唯一性
                                if (Group.length > 0)
                                {
                                    Validate(Group, Callback);
                                }
                                else
                                {
                                    Callback(true);
                                }
                            }
                            else
                            {
                                Callback(true);
                            }
                        }
                        else
                        {
                            //显示验证失败信息
                            V.ShowMessage(Validators.Result);
                            Callback(false);
                        }
                    },
                    Resize: function (State)
                    {
                        switch (State)
                        {
                            case "min":
                                {
                                    //最小化
                                    if (V.Object.Layout == "LR")
                                    {
                                        V.FormContainer.hide();
                                        V.GridContainer.show();
                                        V.GridContainer.width(ContentHeight - 4);
                                        V.Grid.Element.datagrid("resize", { width: ContentHeight - 4 });
                                    }
                                    else
                                    {
                                        V.FormContainer.hide();
                                        V.GridContainer.show();
                                        V.GridContainer.height(ContentHeight);
                                        V.Grid.Element.datagrid("resize", { height: ContentHeight });
                                    }
                                }
                                break;
                            case "max":
                                {
                                    //最大化
                                    if (V.Object.Layout == "LR")
                                    {
                                        V.GridContainer.hide();
                                        V.FormContainer.show();
                                        V.FormContainer.width(ContentHeight - 4);
                                    }
                                    else
                                    {
                                        V.GridContainer.hide();
                                        V.FormContainer.show();
                                        V.FormContainer.height(ContentHeight);
                                        V.FormContainer.find(".group_container").css("max-height", ContentHeight - V.FormContainer.find(".button_container").outerHeight(true) - 4);
                                    }
                                }
                                break;
                            default:
                                {
                                    //正常
                                    if (V.Object.Layout == "LR")
                                    {
                                        V.GridContainer.show();
                                        V.GridContainer.width(GridHeight);
                                        V.Grid.Element.datagrid("resize", { width: GridHeight });
                                        V.FormContainer.show();
                                        V.FormContainer.width(FormHeight - 4);
                                    }
                                    else
                                    {
                                        V.GridContainer.show();
                                        V.GridContainer.height(GridHeight);
                                        V.Grid.Element.datagrid("resize", { height: GridHeight });
                                        V.FormContainer.show();
                                        V.FormContainer.height(FormHeight);
                                        V.FormContainer.find(".group_container").css("max-height", FormHeight - V.FormContainer.find(".button_container").outerHeight(true) - 4);
                                    }
                                }
                                break;
                        }
                    }
                },
			    Render: function (View)
			    {
			        V.Object = View;

			        //localstorage key
			        V.LSK = window.location.pathname + "_" + V.Container.selector; // View.Target;
			        V.LSD = HD.LocalStorage.Get(V.LSK) || {};

			        //增删改按钮
			        if (View.Rights == null || View.Rights == undefined)
			        {
			            View.Rights = "CUD";
			        }

			        if (View.Rights.length > 0)
			        {
			            Buttons.Buttons.push({});

			            if (View.Rights.indexOf("C") != -1)
			            {
			                if (View.Upsert)
			                {
			                    Buttons.Buttons.push({ Command: "insert", Name: "", Tooltip: "重新增加" });
			                    Buttons.Buttons.push({ Command: "upsert", Name: "", Tooltip: "编辑增加" });
			                }
			                else
			                {
			                    Buttons.Buttons.push({ Command: "insert", Name: "", Tooltip: "增加" });
			                }
			            }
			            if (View.Rights.indexOf("D") != -1)
			            {
			                Buttons.Buttons.push({ Command: "delete", Name: "", Tooltip: "删除" });
			            }
			            if (View.Rights.indexOf("U") != -1)
			            {
			                Buttons.Buttons.push({ Command: "update", Name: "", Tooltip: "编辑" });
			            }
			        }

			        Buttons.Buttons.push({});
			        Buttons.Buttons.push({ Command: "export", Name: "", Tooltip: "导出到Excel" });

			        //处理属性列表
			        for (var i = 0, Arr = (View.Properties || View.Propertys), All = View.Property = V.Property, len = Arr.length; i < len; i++)
			        {
			            var P = Arr[i];
			            All[P.Field] = P;
			            if (P.FilterEnabled)
			            {
			                FilterPropertys.push(P);
			            }
			            if (P.OrderEnabled)
			            {
			                OrderPropertys.push(P);
			            }
			            //			            if(P.ColumnEnabled)
			            //			            {
			            //			                ColumnPropertys.push(P);
			            //			            }
			            if (P.Unique)
			            {
			                if (!UniquePropertys)
			                {
			                    UniquePropertys = {};
			                }
			                if (!UniquePropertys[P.Unique])
			                {
			                    UniquePropertys[P.Unique] = [];
			                }
			                UniquePropertys[P.Unique].push(P);
			            }
			        }

			        //生成列索引
			        View.Column = V.Column = {};
			        V.ColumnProperty = {};
			        if (View.FrozenColumns && View.FrozenColumns.length > 0)
			        {
			            for (var i = 0, Arr = View.FrozenColumns, All = View.Column, len = Arr.length; i < len; i++)
			            {
			                for (var j = 0, Cell = Arr[i], lenj = Cell.length; j < lenj; j++)
			                {
			                    if (Cell[j].field)
			                    {
			                        All[Cell[j].field] = Cell[j];
			                        var Cp = { Field: Cell[j].field, Name: Cell[j].title, Frozen: true, Hidden: Cell[j].hidden };
			                        ColumnPropertys.push(Cp);
			                        V.ColumnProperty[Cell[j].field] = Cp;
			                    }
			                }
			            }
			        }
			        if (View.Columns && View.Columns.length > 0)
			        {
			            for (var i = 0, Arr = View.Columns, All = View.Column, len = Arr.length; i < len; i++)
			            {
			                for (var j = 0, Cell = Arr[i], lenj = Cell.length; j < lenj; j++)
			                {
			                    if (Cell[j].field)
			                    {
			                        All[Cell[j].field] = Cell[j];
			                        var Cp = { Field: Cell[j].field, Name: Cell[j].title, Frozen: (Cell[j].locked ? true : false), Hidden: Cell[j].hidden };
			                        ColumnPropertys.push(Cp);
			                        V.ColumnProperty[Cell[j].field] = Cp;
			                    }
			                }
			            }
			        }

			        //生成Form索引
			        if (View.Form)
			        {
			            for (var i = 0, All = V.Field = {}, Arr = View.Form || [], len = Arr.length; i < len; i++)
			            {
			                for (var j = 0, Rows = Arr[i].Inputs || [], lenj = Rows.length; j < lenj; j++)
			                {
			                    for (var j = 0, Rows = Arr[i].Inputs, lenj = Rows.length; j < lenj; j++)
			                    {
			                        for (var k = 0, Cells = Rows[j], lenk = Cells.length; k < lenk; k++)
			                        {
			                            if (Cells[k].Field)
			                            {
			                                All[Cells[k].Field] = Cells[k];
			                            }
			                        }
			                    }
			                }
			            }
			        }

			        //生成Bindings索引
			        for (var i = 0, All = View.Binding = {}, Arr = View.Bindings, len = Arr.length; i < len; i++)
			        {
			            All[Arr[i].Code] = Arr[i].Records;
			        }

			        if (V.BeforeRender)
			        {
			            V.BeforeRender(View, Buttons.Buttons);
			        }

			        jQuery("html,body").css("overflow", "hidden").css("width", "100%").css("height", "100%").css("margin", "0px");
			        switch (View.Layout)
			        {
			            case "LR":
			                {
			                    V.Container.addClass("crud_framework layout_lr").html(Template_LR(jQuery.extend({}, V.Object, Buttons)));
			                }
			                break;
			            case "POP":
			                {
			                    V.Container.addClass("crud_framework layout_dg").html(Template_POP(jQuery.extend({}, V.Object, Buttons)));
			                }
			                break;
			            default:
			                {
			                    V.Container.addClass("crud_framework layout_tb").html(Template_TB(jQuery.extend({}, V.Object, Buttons)));
			                }
			                break;
			        }

			        //初始化各容器高度
			        V.TopContainer = V.Container.find(".top_container");
			        V.FormContainer = V.Form.Container = V.Container.find(".form_container");
			        V.GridContainer = V.Container.find(".grid_container");

			        //绑定按钮事件(文件上传、GIS选点、GIS范围)
			        V.FormContainer.find("button[cmd]").click(function (Evt)
			        {
			            var This = this;
			            if (!jQuery(this).hasClass("disabled"))
			            {
			                var Target = jQuery(this).parents("td").find("input");
			                var Field = V.Field[Target.attr("field")];
			                var Exts = Target.attr("exts");
			                var Regx;
			                if (Exts.length > 0)
			                {
			                    Regx = new RegExp("\.(" + Exts + ")$", "i");
			                }
			                else
			                {
			                    Regx = null;
			                }
			                switch (jQuery(this).attr("cmd"))
			                {
			                    case "upload":
			                        {//文件上传
			                            jQuery(jQuery("#ifm_upload")[0].contentWindow.document.getElementById("file")).unbind("change").change(function ()
			                            {
			                                var File = jQuery("#ifm_upload")[0].contentWindow.document.getElementById("file").value;
			                                if (jQuery(This).attr("hascontent") == "true" && /\.(xls|doc)$/i.test(File))
			                                {
			                                    var Ext = File.match(/\.[a-zA-Z]+$/g);
			                                    jQuery("#ifm_upload")[0].contentWindow.document.getElementById("extend").value = (Ext && jQuery.isArray(Ext) && Ext.length > 0) ? Ext[0] : "";
			                                }
			                                if (File.length > 0)
			                                {
			                                    if (Regx && Regx.test(File) == false)
			                                    {
			                                        V.ShowMessage("请选择扩展名为（" + Exts + "）的文件");
			                                    }
			                                    else
			                                    {
			                                        Loading.Show();
			                                        jQuery("#ifm_upload")[0].contentWindow.document.forms[0].submit();
			                                    }
			                                }
			                            });
			                            jQuery("#ifm_upload").unbind("load").load(function ()
			                            {
			                                if (this.contentWindow.location.pathname == "/upload")
			                                {
			                                    var Result = Proxy.Json.ToObject(this.contentWindow.document.body.innerHTML);
			                                    this.src = this.src;
			                                    var Callback = Field.Uploaded;
			                                    if (jQuery.isFunction(Callback))
			                                    {
			                                        Callback(Result, function (State)
			                                        {
			                                            if (State)
			                                            {
			                                                Target.val(Result.name);
			                                                Target.data("content", Result.content);
			                                            }
			                                        });
			                                    }
			                                    else if (jQuery.type(Callback) === "string" && Callback.length > 0 && jQuery.isFunction(window[Callback]))
			                                    {
			                                        window[Callback](Result, function (State)
			                                        {
			                                            if (State)
			                                            {
			                                                Target.val(Result.name);
			                                                Target.data("content", Result.content);
			                                            }
			                                        });
			                                    }
			                                    else
			                                    {
			                                        Target.val(Result.name);
			                                        Target.data("content", Result.content);
			                                    }
			                                    Loading.Hide();
			                                }
			                            });
			                            jQuery("#ifm_upload")[0].contentWindow.document.getElementById("file").click();
			                        }
			                        break;
			                    case "gispos":
			                        {//GIS选点
			                            //
			                        }
			                        break;
			                    case "gisarea":
			                        {//GIS画区
			                        }
			                        break;
			                }
			            }
			        });

			        //生成快速查询条件区域
			        if (View.Quicks && View.Quicks.length > 0)
			        {
			            for (var i = 0, Eles = V.Container.find(".top_container .left_container>span"), Arr = View.Quicks, len = Arr.length; i < len; i++)
			            {
			                var Quick = Arr[i];
			                //通过Bindings初始化Quick（Combox、AutoComplete）
			                if (Quick.Ext)
			                {
			                    jQuery.extend(true, Quick, Proxy.Json.ToObject(Quick.Ext));
			                    delete Quick.Ext;
			                    if (Quick.Source)
			                    {
			                    	if(Quick.Type=="QComboTree"){
			                    		 Quick.Data = View.Binding[Quick.Source]|| [];
			                    	}else{
			                    		    var None = {};
					                        None[Quick.ValueField || "Id"] = "";
					                        None[Quick.TextField || "Name"] = "不限";
					                        Quick.Data = [None].concat(View.Binding[Quick.Source]) || [];
			                    	}
			                       
			                    }
			                }

			                //调用Quick组件方法生成
			                jQuery(Eles[i])[Quick.Type](Quick);
			            }
			        }

			        //初始化按钮
			        for (var i = 0, Arr = V.Container.find("[command]"), len = Arr.length; i < len; i++)
			        {
			            Button_All[jQuery(Arr[i]).attr("command")] = jQuery(Arr[i]).click(CRUD.Behavior.ButtonClick);
			        }

			        //下拉框初始化
			        BindComboBoxes(View.Bindings || [], V.FormContainer);

			        //combotree初始化
			        V.FormContainer.find("[showtype=combotree]").combotree({ height: 26 });

			        //禁用编辑、删除、确认、取消按钮
			        V.Button.Disable(["update", "delete"]);
			        //禁用表单
			        V.Form.Disable();
			        var GH, CH, GW, FH;
			        var GHeight = 200;
			        if (Options.Grid && jQuery.isNumeric(Options.Grid.MinHeight))
			        {
			            GHeight = Options.Grid.MinHeight;
			        }
			        else
			        {
			            if (Options.Grid)
			            {
			                Options.Grid.MinHeight = GHeight;
			            }
			            else
			            {
			                Options.Grid = { MinHeight: GHeight };
			            }
			        }
			        if (View.Layout == "LR")
			        {//H命名的部分变量复用为宽度值
			            GH = V.Container.height() - V.TopContainer.outerHeight(true) - 4;

			            V.Container.find(">div>div").height(GH);
			            V.Container.find(">div>div.separator_bar").height(GH + 4);

			            CH = ContentHeight = V.Container.width() - 14;
			            var FW;
			            if (V.LSD.FormSize)
			            {
			                FW = FormHeight = V.LSD.FormSize;
			            }
			            else
			            {
			                FW = FormHeight = V.FormContainer.outerWidth(true);
			                if (Options.Form && (Options.Form.Height || Options.Form.Size))
			                {
			                    var FW = FormHeight = Options.Form.Height || Options.Form.Size;
			                }
			                if (FW > CH - GHeight)
			                {
			                    FW = FormHeight = CH - GHeight;
			                }
			                if (FW < V.FormContainer.outerWidth(true))
			                {
			                    V.FormContainer.css("overflow", "auto");
			                }
			            }
			            V.FormContainer.width(FW);
			            FH = FormHeight = V.FormContainer.outerWidth(true);
			            GW = GridHeight = CH - FH - 4;

			            V.FormContainer.find(".group_container").css("max-height", V.FormContainer.height() - V.FormContainer.find(".button_container").outerHeight(true) - 4);
			        }
			        else
			        {
			            CH = ContentHeight = V.Container.height() - V.TopContainer.outerHeight(true) - V.Container.find(".separator_bar").outerHeight(true) - 4;
			            if (V.LSD.FormSize)
			            {
			                FH = FormHeight = V.LSD.FormSize;
			                V.FormContainer.css("overflow-y", "auto");
			                V.FormContainer.height(FH);
			            }
			            else
			            {
			                FH = FormHeight = V.FormContainer.outerHeight(true);
			                if (Options.Form && (Options.Form.Height || Options.Form.Size))
			                {
			                    var FH = FormHeight = Options.Form.Height || Options.Form.Size;
			                }

			                if (FH > CH - GHeight)
			                {
			                    FH = FormHeight = CH - GHeight;
			                    V.FormContainer.css("overflow-y", "auto");
			                    V.FormContainer.height(FH);
			                    FH = FormHeight = V.FormContainer.outerHeight(true);
			                }
			            }

			            GW = V.Container.width() - 4;
			            GH = GridHeight = CH - FH;

			            V.FormContainer.height(V.FormContainer.height());
			            V.FormContainer.find(".group_container").css("max-height", FH - V.FormContainer.find(".button_container").outerHeight(true) - 4);
			        }

			        V.TopContainer.find("button").css("display", "");

			        if (V.AfterRender)
			        {
			            V.AfterRender();
			        }

			        //初始化Grid容器，并进行初次查询
			        if ((!View.Layout || View.Layout == "TB" || View.Layout == "POP") && V.Container.find(".custom_container").length > 0)
			        {
			            var EX_H = (V.Container.find(".custom_container").html()).length > 0 ? (V.Container.find(".custom_container").height() || 32) : 0;
			            var GH = GridHeight = GH - EX_H;
			            V.Container.find(".custom_container").height(EX_H)
			        }
			        V.GridContainer.find("table").width(GW).height(GH);

			        V.Container.find(">.content_container").height(V.Container.height() - V.TopContainer.height() - V.Container.find(".custom_container").height());

			        //--------------------对Columns\FrozenColumns 绑定binding 用于数据字典键值对显示--XJW2015-11-04 ---------//
			        function setBindingFormat(colss)
			        {
			            if (colss)
			            {
			                for (var z = 0; z < colss.length; z++)
			                {
			                    var cols = colss[z];
			                    for (var i = 0; i < cols.length; i++)
			                    {
			                        var col = cols[i];
			                        var ext = col['binding'] || col['ext'];
			                        if ((!col['formatter']) && ext && GBindings)
			                        {
			                            col['formatter'] = eval(col['field'].replace(new RegExp("\\.", "gm"), "_") + 'format=function(Val, R, I) { return _BindingFormatter(Val, R, I, "' + ext + '"); }');
			                        }
			                    }
			                }
			            }
			        }
			        function _BindingFormatter(Val, R, I, E)
			        {
			            var Sources = View.Bindings;
			            for (var j = 0, len = Sources.length; j < len; j++)
			            {
			                if (Sources[j]['Code'] && Sources[j].Code == E)
			                {
			                    var records = Sources[j].Records;
			                    var res = Val;
			                    for (var x = 0; x < records.length; x++)
			                    {
			                        var r = records[x];
			                        if (r['value'] == Val)
			                        {
			                            res = r['name'];
			                        }
			                    }
			                    return res;
			                }
			            }
			        }
			        setBindingFormat(View.FrozenColumns);
			        setBindingFormat(View.Columns);
			        //--------------------对Columns\FrozenColumns 绑定binding 用于数据字典键值对显示-------------------------//

			        V.Grid.Options.frozenColumns = View.FrozenColumns;
			        V.Grid.Options.columns = View.Columns;

			        V.Grid.Element = V.GridContainer.find("table").datagrid(jQuery.extend(true, {}, V.Grid.Options, Options.GridOptions));
			        //设置分页
			        V.Grid.Element.datagrid("getPager").pagination(
                    jQuery.extend(
					{
					    total: 0,
					    showPageList: false,
					    showRefresh: false,
					    beforePageText: "第",
					    afterPageText: "页，共 {pages} 页",
					    displayMsg: "从 {from} 到 {to} 共 {total} 条"
					}, Options.Pagination));

			        //绑定中间分隔条按钮事件
			        V.Container.find(".separator_bar>div").click(function (Evt)
			        {
			            V.Form.Resize(jQuery(this).attr("state"));
			        });

			        //绑定中间分隔条拖动事件
			        V.Container.find(">.content_container").mouseup(MouseUp);

			        V.Container.find(">.content_container>.separator_bar").css("cursor", V.Object.Layout == "LR" ? "w-resize" : "s-resize").mousedown(MouseDown);

			        if (V.Form.Auto)
			        {
			            V.Form.Resize(V.Form.Auto.Query);
			        }

			        //绑定页面Resize事件
			        //jQuery(window).resize(function(Evt)
			        //{
			        //   Cmp.Grid.Object.datagrid("resize", { width: V.Container.width() });
			        //});

			        //添加上传页面
			        if (jQuery("#ifm_upload").length == 0)
			        {
			            jQuery("<iframe id=\"ifm_upload\" src=\"" + V.Core.Path + "hUpload.htm\" style=\"display:none;\"></iframe>").appendTo(document.body);
			        }

			        //V.SetSettings(HD.LocalStorage.Get(V.LSK) || V.GetSettings()); 
			        V.SetSettings(V.GetSettings()); //--XJW 缓存中的字段名修改掉会报错，暂不取缓存
			    },
			    ShowMessage: function (Message, Callback)
			    {
			        V.Context.ShowDialog({ Title: "提示", Type: window.top.MyDialog.Types.Message, Icon: window.top.MyDialog.Icons.Info, Message: Message }, null, Callback);
			    },
			    ShowConfirm: function (Message, Callback)
			    {
			        V.Context.ShowDialog({ Title: "提示", Type: window.top.MyDialog.Types.Confirm, Icon: window.top.MyDialog.Icons.Question, Message: Message }, null, Callback);
			    },
			    ShowDialog: function (Options, Params, Callback)
			    {
			        V.Context.ShowDialog(jQuery.extend({ Title: "对话框", Url: "", Width: 400, Height: 300 }, Options), Params, Callback);
			    },
			    ShowWait: function ()
			    {
			        V.Context.jQuery.messager.progress({ text: "请稍候" });
			    },
			    CloseWait: function ()
			    {
			        V.Context.jQuery.messager.progress("close");
			    },
			    Reset: function (Options)
			    {
			        if (Options)
			        {
			            //重新设置Filters、Orders、Columns
			            //处理属性列表
			            V.Object.Properties = Options.Properties;
			            FilterPropertys = [];
			            OrderPropertys = [];
			            UniquePropertys = {};
			            V.Object.Property = {};
			            Filters = [];
			            Orders = [];
			            for (var i = 0, Arr = (V.Object.Properties || V.Object.Propertys), All = V.Object.Property = V.Property, len = Arr.length; i < len; i++)
			            {
			                var P = Arr[i];
			                All[P.Field] = P;
			                if (P.FilterEnabled)
			                {
			                    FilterPropertys.push(P);
			                }
			                if (P.OrderEnabled)
			                {
			                    OrderPropertys.push(P);
			                }
			                if (P.Unique)
			                {
			                    if (!UniquePropertys)
			                    {
			                        UniquePropertys = {};
			                    }
			                    if (!UniquePropertys[P.Unique])
			                    {
			                        UniquePropertys[P.Unique] = [];
			                    }
			                    UniquePropertys[P.Unique].push(P);
			                }
			            }

			            //生成列索引
			            ColumnPropertys = [];
			            V.Object.Column = V.Column = {};
			            V.ColumnProperty = {};
			            for (var i = 0, Arr = Options.FrozenColumns, All = V.Object.Column, len = Arr.length; i < len; i++)
			            {
			                for (var j = 0, Cell = Arr[i], lenj = Cell.length; j < lenj; j++)
			                {
			                    if (Cell[j].field)
			                    {
			                        All[Cell[j].field] = Cell[j];
			                        var Cp = { Field: Cell[j].field, Name: Cell[j].title, Frozen: true, Hidden: Cell[j].hidden };
			                        ColumnPropertys.push(Cp);
			                        V.ColumnProperty[Cell[j].field] = Cp;
			                    }
			                }
			            }
			            for (var i = 0, Arr = Options.Columns, All = V.Object.Column, len = Arr.length; i < len; i++)
			            {
			                for (var j = 0, Cell = Arr[i], lenj = Cell.length; j < lenj; j++)
			                {
			                    if (Cell[j].field)
			                    {
			                        All[Cell[j].field] = Cell[j];
			                        var Cp = { Field: Cell[j].field, Name: Cell[j].title, Frozen: (Cell[j].locked ? true : false), Hidden: Cell[j].hidden };
			                        ColumnPropertys.push(Cp);
			                        V.ColumnProperty[Cell[j].field] = Cp;
			                    }
			                }
			            }
			        }
			        else
			        {
			            Filters = [];
			            Orders = [];
			            for (var i = 0, len = ColumnPropertys.length, Grid = V.Grid.Element; i < len; i++)
			            {
			                ColumnPropertys[i].Hidden = false;
			                if (ColumnPropertys[i].Field && V.Column[ColumnPropertys[i].Field])
			                {
			                    V.Column[ColumnPropertys[i].Field].hidden = false;
			                }
			                Grid.datagrid("showColumn", ColumnPropertys[i].Field);
			            }
			        }
			    },
			    GetSettings: function ()
			    {
			        return { Filters: Filters, Orders: Orders, Columns: ColumnPropertys };
			    },
			    SetSettings: function (Settings)
			    {
			        if (jQuery.isArray(Settings.Filters))
			        {
			            Filters = Settings.Filters;
			        }
			        if (jQuery.isArray(Settings.Orders))
			        {
			            Orders = Settings.Orders;
			        }
			        if (jQuery.isArray(Settings.Columns))
			        {
			            ColumnPropertys = Settings.Columns;
			        }
			    },
			    ShowFilter: function (Arguments, Callback)
			    {
					if (CRUD.Behavior.Button&&CRUD.Behavior.Button.BeforeShowFilter){
						CRUD.Behavior.Button.BeforeShowFilter(Filters);
					}
			        V.Context.ShowDialog({ Title: "过滤", Url: this.Core.Path.replace("CRUD/", "Filter/DlgFilter.htm"), Width: 530, Height: 360 },
			            { Fields: FilterPropertys, Bindings: V.Object.Bindings, Filters: Filters },
                        function (Result)  
                        {
                            if (Result)
                            {
                                Filters = [].concat(Result);
                                Filters.Merge = FilterMerge;
                                Filters.Clear = FilterClear;
                                Callback(Result);
                            }
                        });
			    },
			    ShowOrder: function (Arguments, Callback)
			    {
			        V.Context.ShowDialog({ Title: "排序", Url: this.Core.Path.replace("CRUD/", "Order/DlgOrder.htm"), Width: 580, Height: 360 },
			            { Fields: OrderPropertys, Orders: Orders },
                        function (Result)
                        {
                            if (Result)
                            {
                                Orders = [].concat(Result);
                                Orders.Merge = OrderMerge;
                                Orders.Clear = OrderClear;
                                /*/排序字段显示
                                for(var i = 0, len = Result.length, Grid = V.Grid.Element; i < len; i++)
                                {
                                Grid.datagrid("showColumn", Result[i].Field);
                                V.Column[Result[i].Field].hidden = false;
                                }//*/

                                Callback(Result);
                            }
                        });
			    },
			    ShowColumn: function (Arguments, Callback)
			    {
			        V.Context.ShowDialog({ Title: "列定义", Url: this.Core.Path.replace("CRUD/", "Column/DlgColumn.htm"), Width: 350, Height: 360 },
			            { Fields: ColumnPropertys },
                        function (Result)
                        {
                            if (Result)
                            {
                                var State = false;
                                for (var i = 0, len = Result.length, Grid = V.Grid.Element; i < len; i++)
                                {
                                    if (Result[i].Hidden)
                                    {
                                        Grid.datagrid("hideColumn", Result[i].Field);
                                        V.Column[Result[i].Field].hidden = true;
                                        State = true;
                                    }
                                    else
                                    {
                                        Grid.datagrid("showColumn", Result[i].Field);
                                        V.Column[Result[i].Field].hidden = false;
                                    }
                                }
                                //保存localstorage
                                //HD.LocalStorage.Set(V.LSK, V.GetSettings(), 7 * 24 * 3600);

                                Callback(State);
                            }
                        });
			    },
			    QuickFilter: function (Arguments, Callback)
			    {
			        Filters = [];
			        Filters.Merge = FilterMerge;
			        Filters.Clear = FilterClear;
			        if (V.Object.Quicks.length > 0)
			        {
			            for (var i = 0, Arr = V.Container.find(".left_container>span.quick").Quick().Get(), len = Arr.length; i < len; i++)
			            {
			                var Quick = Arr[i];
			                if (Quick.Value != undefined)
			                {
			                    if (Quick.Type == "QText")
			                    {
			                        if (Quick.Value)
			                        {
			                            Filters.push({ Field: Quick.Field, Value: Quick.Value, Operate: "like", Relation: "and" });
			                        }
			                    }
			                    else
			                    {
			                        if (V.Property && V.Property[Quick.Field] && V.Property[Quick.Field].ShowType == "datetime" && V.Property[Quick.Field].DataType == "Number" && Quick.Value)
			                        {
			                            Filters.push({ Field: Quick.Field, Value: ConvertToDate(Quick.Value, Quick.Format).getTime() / 1000, Operate: (V.Property[Quick.Field].Operate || "="), Relation: "and" });
			                        }
			                        else if (Quick.Value)
			                        {
			                            if (V.Property[Quick.Field].DataType == "Number")
			                            {
			                                Filters.push({ Field: Quick.Field, Value: Number(Quick.Value), Operate: (V.Property[Quick.Field].Operate || "="), Relation: "and" });
			                            }
			                            else
			                            {
			                                Filters.push({ Field: Quick.Field, Value: Quick.Value, Operate: (V.Property[Quick.Field].Operate || "="), Relation: "and" });
			                            }
			                        }
			                    }
			                }
			                if (Quick.Min != undefined)
			                {
			                    if (Quick.Min)
			                    {
			                        Filters.push({ Field: Quick.Field, Value: Quick.Min, Operate: ">=", Relation: "and" });
			                    }
			                    if (Quick.Max)
			                    {
			                        Filters.push({ Field: Quick.Field, Value: Quick.Max, Operate: "<=", Relation: "and" });
			                    }
			                }
			                if (Quick.Begin != undefined)
			                {
			                    if (V.Property[Quick.Field].DataType == "Number")
			                    {
			                        if (Quick.Begin)
			                        {
			                            Filters.push({ Field: Quick.Field, Value: ConvertToDate(Quick.Begin, Quick.Format).getTime() / 1000, Operate: ">=", Relation: "and" });
			                        }
			                        if (Quick.End)
			                        {
			                            Filters.push({ Field: Quick.Field, Value: ConvertToDate(Quick.End, Quick.Format).getTime() / 1000, Operate: "<=", Relation: "and" });
			                        }
			                    }
			                    else
			                    {
			                        if (Quick.Begin)
			                        {
			                            Filters.push({ Field: Quick.Field, Value: Quick.Begin, Operate: ">=", Relation: "and" });
			                        }
			                        if (Quick.End)
			                        {
			                            Filters.push({ Field: Quick.Field, Value: Quick.End, Operate: "<=", Relation: "and" });
			                        }
			                    }
			                }
			            }
			        }
			        Callback(Filters);
			    },
			    DialogForm: function (Container, Record)
			    {

			        var Dlg = CRUD.View.Dialog = this;

			        Container.css("max-height", jQuery(window).height() - 60).addClass("crud_framework").html(template.compile(jQuery.GetTemplate(function ()
			        {
			            /*
			            <div class="form_container">
			            <div class="group_container">
			            {{include "crud_temp_form"}}
			            </div>
			            <div class="button_container">
			            <button command="confirm" class="confirm" type="button">确定</button>
			            <button command="cancel" type="button" >取消</button>
			            </div>
			            </div>
			            */
			        }), { escape: false })(V.Object));
			        if (Container.prop("scrollHeight") > Container.prop("clientHeight"))
			        {
			            Container.css("overflow", "auto");
			        }

			        BindComboBoxes(V.Object.Bindings || [], Container);

			        //绑定按钮事件(文件上传、GIS选点、GIS范围)
			        Container.find("button[cmd]").click(function (Evt)
			        {
			            if (!jQuery(this).hasClass("disabled"))
			            {
			                var Target = jQuery(this).parents("td").find("input");
			                var Field = V.Field[Target.attr("field")];
			                var Exts = Target.attr("exts");
			                var Regx;
			                if (Exts.length > 0)
			                {
			                    Regx = new RegExp("\.(" + Exts + ")$", "i");
			                }
			                else
			                {
			                    Regx = null;
			                }
			                switch (jQuery(this).attr("cmd"))
			                {
			                    case "upload":
			                        {//文件上传
			                            jQuery(jQuery("#ifm_upload")[0].contentWindow.document.getElementById("file")).unbind("change").change(function ()
			                            {
			                                var File = jQuery("#ifm_upload")[0].contentWindow.document.getElementById("file").value;
			                                if (jQuery(this).attr("hascontent") == "true" && /\.(xls|doc)$/i.test(File))
			                                {
			                                    var Ext = File.match(/\.[a-zA-Z]+$/g);
			                                    jQuery("#ifm_upload")[0].contentWindow.document.getElementById("extend").value = (Ext && jQuery.isArray(Ext) && Ext.length > 0) ? Ext[0] : "";
			                                }
			                                if (File.length > 0)
			                                {
			                                    if (Regx && Regx.test(File) == false)
			                                    {
			                                        V.ShowMessage("请选择扩展名为（" + Exts + "）的文件");
			                                    }
			                                    else
			                                    {
			                                        Loading.Show();
			                                        jQuery("#ifm_upload")[0].contentWindow.document.forms[0].submit();
			                                    }
			                                }
			                            });
			                            jQuery("#ifm_upload").unbind("load").load(function ()
			                            {
			                                if (this.contentWindow.location.pathname == "/upload")
			                                {
			                                    var Result = Proxy.Json.ToObject(this.contentWindow.document.body.innerHTML);
			                                    this.src = this.src;
			                                    var Callback = Field.Uploaded;
			                                    if (jQuery.isFunction(Callback))
			                                    {
			                                        Callback(Result, function (State)
			                                        {
			                                            if (State)
			                                            {
			                                                Target.val(Result.name);
			                                                Target.data("content", Result.content);
			                                            }
			                                        });
			                                    }
			                                    else if (jQuery.type(Callback) === "string" && Callback.length > 0 && jQuery.isFunction(window[Callback]))
			                                    {
			                                        window[Callback](Result, function (State)
			                                        {
			                                            if (State)
			                                            {
			                                                Target.val(Result.name);
			                                                Target.data("content", Result.content);
			                                            }
			                                        });
			                                    }
			                                    else
			                                    {
			                                        Target.val(Result.name);
			                                        Target.data("content", Result.content);
			                                    }
			                                    Loading.Hide();
			                                }
			                            });
			                            jQuery("#ifm_upload")[0].contentWindow.document.getElementById("file").click();
			                        }
			                        break;
			                    case "gispos":
			                        {//GIS选点
			                            //
			                        }
			                        break;
			                    case "gisarea":
			                        {//GIS画区
			                        }
			                        break;
			                }
			            }
			        });

			        V.FormContainer = Container.find(".form_container");
			        CRUD.View.Form.Set(MyDialog.Arguments.Command);

			        Container.find("button[command=cancel]").click(function (Evt)
			        {
			            MyDialog.Close();
			        });
			        Container.find("button[command=confirm]").click(function (Evt)
			        {
			            MyDialog.Arguments.Save(function (Result)
			            {
			                MyDialog.Close();
			                MyDialog.Arguments.Success(Result);
			            });
			        });
			    }
			};
	        if (Options.Context)
	        {
	            V.Context = Options.Context;
	        }

	        if (Options.Form && Options.Form.Auto)
	        {
	            V.Form.Auto = Options.Form.Auto;
	        }

	        //render
	        if (jQuery.isFunction(Options.BeforeRender))
	        {
	            V.BeforeRender = Options.BeforeRender;
	        }
	        if (jQuery.isFunction(Options.AfterRender))
	        {
	            V.AfterRender = Options.AfterRender;
	        }
	        //form.clear
	        if (Options.Form && jQuery.isFunction(Options.Form.BeforeClear))
	        {
	            V.Form.BeforeClear = Options.Form.BeforeClear;
	        }
	        if (Options.Form && jQuery.isFunction(Options.Form.AfterClear))
	        {
	            V.Form.AfterClear = Options.Form.AfterClear;
	        }
	        //form.enable
	        if (Options.Form && jQuery.isFunction(Options.Form.BeforeEnable))
	        {
	            V.Form.BeforeEnable = Options.Form.BeforeEnable;
	        }
	        if (Options.Form && jQuery.isFunction(Options.Form.AfterEnable))
	        {
	            V.Form.AfterEnable = Options.Form.AfterEnable;
	        }
	        //form.disable
	        if (Options.Form && jQuery.isFunction(Options.Form.BeforeDisable))
	        {
	            V.Form.BeforeDisable = Options.Form.BeforeDisable;
	        }
	        if (Options.Form && jQuery.isFunction(Options.Form.AfterDisable))
	        {
	            V.Form.AfterDisable = Options.Form.AfterDisable;
	        }
	        //form.get
	        if (Options.Form && jQuery.isFunction(Options.Form.BeforeGet))
	        {
	            V.Form.BeforeGet = Options.Form.BeforeGet;
	        }
	        if (Options.Form && jQuery.isFunction(Options.Form.AfterGet))
	        {
	            V.Form.AfterGet = Options.Form.AfterGet;
	        }
	        //form.set
	        if (Options.Form && jQuery.isFunction(Options.Form.BeforeSet))
	        {
	            V.Form.BeforeSet = Options.Form.BeforeSet;
	        }
	        if (Options.Form && jQuery.isFunction(Options.Form.AfterSet))
	        {
	            V.Form.AfterSet = Options.Form.AfterSet;
	        }

	        if (Options.Grid && jQuery.isFunction(Options.Grid.AfterLoad))
	        {
	            V.Grid.AfterLoad = Options.Grid.AfterLoad;
	        }

	        return V;
	    }
	});
//})(jQuery);