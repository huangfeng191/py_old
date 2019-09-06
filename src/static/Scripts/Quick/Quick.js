; (function(jQuery)
{
    //jQuery.ImplantStyle("Quick", "Default");

    //注入样式
    var Script = jQuery("script[src$='/Quick.js']");
    var Skin = Script.attr("skin") || "Default";
    Script.after("<link href=\"" + Script.attr("src").replace("Quick.js", "Skins/" + Skin + "/skin.css") + "\" rel=\"stylesheet\" type=\"text/css\" />");

    function GetOptions(Default, Element, Options)
    {
        var Opts = jQuery.extend(true, {}, Default);

        for(var Key in Opts)
        {
            if(Key == "Data")
            {
                Opts[Key] = window[Element.attr("_" + Key.toLowerCase())] || Opts[Key];
            }
            else if(Key.indexOf("On") == 0)
            {
                Opts[Key] = window[Element.attr("_" + Key.toLowerCase())] || Opts[Key];
            }
            else
            {
                Opts[Key] = Element.attr("_" + Key.toLowerCase()) || Opts[Key];
            }
        }

        jQuery.extend(true, Opts, Options);

        return Opts;
    };
    function CommonGet(Index)
    {
        var Records = [];
        this.each(function(Index, Ele)
        {
            Records.push({ Type: jQuery(Ele).data("options").Type, Field: jQuery(Ele).data("options").Field, Value: jQuery(Ele).find("input").val() });
        });
        if(jQuery.isNumeric(Index) && Index < Records.length && Index >= 0)
        {
            return Records[Index];
        }
        else
        {
            return Records;
        }
    };
    function CommonSet(Value)
    {
        this.each(function(Index, Ele)
        {
            jQuery(Ele).find("input.value").val(Value);
        });
    };
    function CommonShow()
    {
        this.show();
    };
    function CommonHide()
    {
        this.hide();
    };
    function CommonEnable()
    {
        this.find("input.value").removeAttr("disabled");
    };
    function CommonDisable()
    {
        this.find("input.value").attr("disabled", "disabled");
    };

    var QTypes = {};

    jQuery.extend({ QTypes: QTypes });

    //文本
    var QText = QTypes["QText"] =
	{
	    Options:
		{
		    Type: "QText",
		    Label: "",
            Suffix: "",
		    Field: "",
		    Value: "",
		    Width: 0
		},
	    Template: template.compile(jQuery.GetTemplate(function()
	    {
	        /*
	        <span class="label">{{Label}}</span>
	        <input type="text" class="value"{{if Width > 0}} style="width:{{Width}}px;"{{/if}} value="{{Value}}" />
            <span class="suffix">{{Suffix}}</span>
	        */
	    })),
	    Get: CommonGet,
	    Set: CommonSet,
	    Show: CommonShow,
	    Hide: CommonHide,
	    Enable: CommonEnable,
	    Disable: CommonDisable
	};
    //下拉框
    var QCombox = QTypes["QCombox"] =
	{
	    Options:
        {
            Type: "QCombox",
            Label: "",
            Suffix: "",
            Field: "",
            Value: "",
            Data: [],
            TextField: "Name",
            Multiple: false,
            ValueField: "Id",
            Editable: false,
            Width: "auto",
            Height: 26,
            OnSelect: function() { },
            PanelWidth: null,
            OnLoadSuccess: function() { },
            Formatter: null
        },
	    Template: template.compile(jQuery.GetTemplate(function()
	    {
	        /*
	        <span class="label">{{Label}}</span>
	        <input type="text" class="value" />
            <span class="suffix">{{Suffix}}</span>
	        */
	    })),
	    Get: function(Index)
	    {
	        var Records = [];
	        this.each(function(Index, Ele)
	        {
	            if(jQuery(Ele).data("options").Multiple)
	            {
	                Records.push({ Type: "QCombox", Field: jQuery(Ele).data("options").Field, Value: jQuery(Ele).find("input").combobox("getValues"), Text: jQuery(Ele).find("input").combobox("getText") });
	            } 
                else
	            {
	                Records.push({ Type: "QCombox", Field: jQuery(Ele).data("options").Field, Value: jQuery(Ele).find("input").combobox("getValue"), Text: jQuery(Ele).find("input").combobox("getText") });
	            }
	        });
	        if(jQuery.isNumeric(Index) && Index < Records.length && Index >= 0)
            {
                return Records[Index];
            }
            else
            {
                return Records;
            }
	    },
	    Set: function(Value)
	    {
	        this.each(function(Index, Ele)
	        {
	            if(jQuery(Ele).data("options").Multiple)
	            {
	                jQuery(Ele).find("input.value").combobox("setValues", Value);
	            } else
	            {
	                jQuery(Ele).find("input.value").combobox("setValue", Value);
	            }
	        });
	    },
	    Show: CommonShow,
	    Hide: CommonHide,
	    Enable: function()
	    {
	        this.each(function(Index, Ele)
	        {
	            jQuery(Ele).find("input.value").combobox("enable");
	        });
	    },
	    Disable: function()
	    {
	        this.each(function(Index, Ele)
	        {
	            jQuery(Ele).find("input.value").combobox("disable");
	        });
	    }
	};
    //日期框
    var QDatetime = QTypes["QDatetime"] =
	{
	    Options:
		{
		    Type: "QDatetime",
		    Label: "",
            Suffix: "",
		    Field: "",
		    Value: "",
		    Format: "yyyy-MM-dd",
		    Operator: true,
		    ShowToday: true,
		    ShowClear: true,
		    OnChange: null
		},

	    Template: template.compile(jQuery.GetTemplate(function()
	    {
	        /*
	        <span class="label">{{Label}}</span>
	        <input type="text" class="data value {{Format.replace(/[-:\s]/g,"")}}" value="{{Value}}" onclick="new WdatePicker({skin:'default',readOnly:true,isShowToday:{{if ShowToday == true}}true{{else}}false{{/if}},isShowClear:{{if ShowClear == true}}true{{else}}false{{/if}},dateFmt:'{{Format}}'{{if OnChange}},onpicked: QuickDateTimeChanged,oncleared: QuickDateTimeChanged{{/if}}})" />
	        {{if Operator == true}}<div class="operator"><div class="prev"></div><div class="next"></div></div>{{/if}}
            <span class="suffix">{{Suffix}}</span>
	        */
	    })),
	    Get: function(Index)
	    {
	        var Records = [];
	        this.each(function(Index, Ele)
	        {
	            Records.push({ Type: "QDatetime", Field: jQuery(Ele).data("options").Field, Value: jQuery(Ele).find("input").val(), Format: jQuery(Ele).data("options").Format });
	        });
	        if(jQuery.isNumeric(Index) && Index < Records.length && Index >= 0)
            {
                return Records[Index];
            }
            else
            {
                return Records;
            }
	    },
	    Set: CommonSet,
	    Show: CommonShow,
	    Hide: CommonHide,
	    Enable: function()
	    {
	        this.find("input.value, div.operator>div").removeAttr("disabled");
	    },
	    Disable: function()
	    {
	        this.find("input.value, div.operator>div").attr("disabled", "disabled");
	    }
	};
    //时刻框
    var QTimePicker = QTypes["QTimePicker"] =
    {
        Options:
        {
            Type: "QTimePicker",
            Label: "",
            Suffix: "",
            Field: "",
            Value: "00:00",
            Operator: true
        },
        Template: template.compile(jQuery.GetTemplate(function()
        {
            /*
            <span class="label">{{Label}}</span>
            <span class="input"><input type="text" class="value hh" maxlength="2" value="{{Value.split(":")[0]}}" /><span class="label">:</span><input type="text" class="value mm" maxlength="2" value="{{Value.split(":")[1]}}" /></span>
            {{if Operator == true}}<div class="operator"><div class="prev"></div><div class="next"></div></div>{{/if}}
            <span class="suffix">{{Suffix}}</span>
            */
        })),
        Get: function(Index)
        {
            var Records = [];
            this.each(function(Index, Ele)
            {
                Records.push({ Type: "QTimePicker", Field: jQuery(Ele).data("options").Field, Value: jQuery(Ele).find("input.hh").val() + ":" + jQuery(Ele).find("input.mm").val() });
            });
            if(jQuery.isNumeric(Index) && Index < Records.length && Index >= 0)
            {
                return Records[Index];
            }
            else
            {
                return Records;
            }
        },
        Set: function(Value)
        {
            Vals = Value.split(":");
            this.each(function(Index, Ele)
            {
                jQuery(Ele).find("input.hh").val(Vals[0]);
                jQuery(Ele).find("input.mm").val(Vals[1]);
            });
        },
        Show: CommonShow,
        Hide: CommonHide,
        Enable: function()
        {
            this.find("input.value, div.operator>div").removeAttr("disabled");
        },
        Disable: function()
        {
            this.find("input.value, div.operator>div").attr("disabled", "disabled");
        }
    };
    //自动完成
    var QAutoComplete = QTypes["QAutoComplete"] =
	{
	    Options:
		{
		    Type: "QAutoComplete",
		    Label: "",
            Suffix: "",
		    Field: "",
		    Value: "",
		    Data: [],
		    Max: 10,
		    MinChars: 1,
		    MustMatch: false,
		    MatchContains: true,
		    MatchCase: false,
		    AutoFill: false,
		    Scroll: true,
		    OnFormatItem: function(Item)
		    {
		        return Item[0];
		    },
		    OnFormatMatch: function(Item)
		    {
		        return Item[0];
		    },
		    OnFormatResult: function(Item)
		    {
		        return Item[0];
		    },
		    OnCallback: function(Evt, Item)
		    {
		    }
		},
	    Template: template.compile(jQuery.GetTemplate(function()
	    {
	        /*
	        <span class="label">{{Label}}</span>
	        <input type="text" class="value" value="{{Value}}" />
            <span class="suffix">{{Suffix}}</span>
	        */
	    })),
	    Get: CommonGet,
	    Set: CommonSet,
	    Show: CommonShow,
	    Hide: CommonHide,
	    Enable: CommonEnable,
	    Disable: CommonDisable
	};
    //数值框
    var QNumber = QTypes["QNumber"] =
	{
	    Options:
		{
		    Type: "QNumber",
		    Label: "",
            Suffix: "",
		    RightLabel: "",
		    Field: "",
		    Value: "",
		    Width: 120,
		    Digits: null
		},
	    Template: template.compile(jQuery.GetTemplate(function()
	    {
	        /*
	        <span class="label">{{Label}}</span>
	        <input type="text" class="value" value="{{Value}}" style="width:{{Width}}px;" />
	        {{if RightLabel}}<span class="label">{{RightLabel}}</span>{{/if}}
            <span class="suffix">{{Suffix}}</span>
	        */
	    })),
	    Get: function(Index)
	    {
	        var Records = [];
	        this.each(function(Index, Ele)
	        {
	        	var Val = jQuery(Ele).find("input").val();
	            Records.push({ Type: "QNumber", Field: jQuery(Ele).data("options").Field, Value: $.isNumeric(Val) ? Number(Val) : (Val ? NaN : null) });
	        });
	        if(jQuery.isNumeric(Index) && Index < Records.length && Index >= 0)
            {
                return Records[Index];
            }
            else
            {
                return Records;
            }
	    },
	    Set: function(Value)
	    {
	        if(!jQuery.isNumeric(Value))
	        {
	            Value = "";
	        }
	        this.each(function(Index, Ele)
	        {
	            jQuery(Ele).find("input").val(Value);
	        });
	    },
	    Show: CommonShow,
	    Hide: CommonHide,
	    Enable: CommonEnable,
	    Disable: CommonDisable
	};
    //数值范围
    var QNumberRange = QTypes["QNumberRange"] =
	{
	    Options:
		{
		    Type: "QNumberRange",
		    Label: "",
            Suffix: "",
		    Field: "",
		    Seperator: "-",
		    Digits: null,
		    Min: "",
		    Max: ""
		},
	    Template: template.compile(jQuery.GetTemplate(function()
	    {
	        /*
	        <span class="label">{{Label}}</span>
	        <input type="text" class="value v1" style="width:{{Width}}px;" value="{{Min}}" />
	        <span class="label">{{Seperator}}</span>
	        <input type="text" class="value v2" style="width:{{Width}}px;" value="{{Max}}" />
            <span class="suffix">{{Suffix}}</span>
	        */
	    })),
	    Get: function(Index)
	    {
	        var Records = [];
	        this.each(function(Index, Ele)
	        {
                var Min = jQuery(Ele).find("input.v1").val();
                if(jQuery.isNumeric(Min))
                {
                    Min = Number(Min);
                }
                else if(Min)
                {
                    Min = NaN;
                }
                else
                {
                    Min = null;
                }
                var Max = jQuery(Ele).find("input.v2").val();
                if(jQuery.isNumeric(Max))
                {
                    Max = Number(Max);
                }
                else if(Max)
                {
                    Max = NaN;
                }
                else
                {
                    Max = null
                }
	            Records.push({ Type: "QNumberRange", Field: jQuery(Ele).data("options").Field, Min: Min, Max: Max });
	        });
	        if(jQuery.isNumeric(Index) && Index < Records.length && Index >= 0)
            {
                return Records[Index];
            }
            else
            {
                return Records;
            }
	    },
	    Set: function(Min, Max)
	    {
	        if(!jQuery.isNumeric(Min))
	        {
	            Min = "";
	        }
	        if(!jQuery.isNumeric(Max))
	        {
	            Max = "";
	        }
	        this.each(function(Index, Ele)
	        {
	            jQuery(Ele).find("input.v1").val(Min);
	            jQuery(Ele).find("input.v2").val(Max);
	        });
	    },
	    Show: CommonShow,
	    Hide: CommonHide,
	    Enable: CommonEnable,
	    Disable: CommonDisable
	};
    //日期范围
    var QDatetimeRange = QTypes["QDatetimeRange"] =
	{
	    Options:
		{
		    Type: "QDatetimeRange",
		    Label: "",
            Suffix: "",
		    Field: "",
		    Format: "yyyy-MM-dd",
		    Operator: true,
		    ShowToday: true,
		    ShowClear: true,
		    Seperator: "-",
		    Begin: "",
		    End: ""
		},
	    Template: template.compile(jQuery.GetTemplate(function()
	    {
	        /*
	        <span class="label">{{Label}}</span>
	        <input id="drb_{{Id}}" type="text" class="data value v1 {{Format.replace(/[-:\s]/g,"")}}" value="{{Begin}}" onclick="new WdatePicker({skin:'default',readOnly:true,isShowToday:{{if ShowToday == true}}true{{else}}false{{/if}},isShowClear:{{if ShowClear == true}}true{{else}}false{{/if}},dateFmt:'{{Format}}',maxDate:'#F{$dp.$D(\'dre_{{Id}}\')}'})" />
	        {{if Operator == true}}<div class="operator"><div class="prev v1"></div><div class="next v1"></div></div>{{/if}}
	        <span class="label">{{Seperator}}</span>
	        <input id="dre_{{Id}}" type="text" class="data value v2 {{Format.replace(/[-:\s]/g,"")}}" value="{{End}}" onclick="new WdatePicker({skin:'default',readOnly:true,isShowToday:{{if ShowToday == true}}true{{else}}false{{/if}},isShowClear:{{if ShowClear == true}}true{{else}}false{{/if}},dateFmt:'{{Format}}',minDate:'#F{$dp.$D(\'drb_{{Id}}\')}'})" />
	        {{if Operator == true}}<div class="operator"><div class="prev v2"></div><div class="next v2"></div></div>{{/if}}
            <span class="suffix">{{Suffix}}</span>
	        */
	    })),
	    Get: function(Index)
	    {
	        var Records = [];
	        this.each(function(Index, Ele)
	        {
	            Records.push({ Type: "QDatetimeRange", Field: jQuery(Ele).data("options").Field, Begin: jQuery(Ele).find("input.v1").val(), End: jQuery(Ele).find("input.v2").val(), Format: jQuery(Ele).data("options").Format });
	        });
	        if(jQuery.isNumeric(Index) && Index < Records.length && Index >= 0)
            {
                return Records[Index];
            }
            else
            {
                return Records;
            }
	    },
	    Set: function(Begin, End)
	    {
	        this.each(function(Index, Ele)
	        {
	            jQuery(Ele).find("input.v1").val(Begin);
	            jQuery(Ele).find("input.v2").val(End);
	        });
	    },
	    Show: CommonShow,
	    Hide: CommonHide,
	    Enable: function()
	    {
	        this.find("input.value, div.operator>div").removeAttr("disabled");
	    },
	    Disable: function()
	    {
	        this.find("input.value, div.operator>div").attr("disabled", "disabled");
	    }
	};
    //复选框
    var QCheckbox = QTypes["QCheckbox"] =
	{
	    Options:
        {
            Type: "QCheckbox",
            Label: "",
            Suffix: "",
            Field: "",
            Value: false
        },
	    Template: template.compile(jQuery.GetTemplate(function()
	    {
	        /*
	        <input type="checkbox" class="value" {{if Value}}checked="checked"{{/if}} />
	        <span class="label">{{Label}}</span>
	        */
	    })),
	    Get: function(Index)
	    {
	        var Records = [];
	        this.each(function(Index, Ele)
	        {
	            Records.push({ Type: "QCheckbox", Field: jQuery(Ele).data("options").Field, Value: (jQuery(Ele).find("input:checked").length > 0) });
	        });
	        if(jQuery.isNumeric(Index) && Index < Records.length && Index >= 0)
            {
                return Records[Index];
            }
            else
            {
                return Records;
            }
	    },
	    Set: function(Value)
	    {
	        this.each(function(Index, Ele)
	        {
	            jQuery(Ele).find("input.value").prop("checked", Value);
	        });
	    },
	    Show: CommonShow,
	    Hide: CommonHide,
	    Enable: CommonEnable,
	    Disable: CommonDisable
	};
    //下拉树
    var QComboTree = QTypes["QComboTree"] =
    {
        Options:
        {
            Type: "QComboTree",
            Label: "",
            Suffix: "",
            Field: "",
            Value: null,
            Width: 120,
            Height: 26,
            PanelWidth: null,
            PanelHeight: 200,
            Data: [],
            ShowCheckbox: false,
            Multiple: false,
            OnlyLeafCheck: false,
            OnClick: null
        },
        Template: template.compile(jQuery.GetTemplate(function()
        {
            /*
            <span class="label">{{Label}}</span>
            <input type="text" class="value" />
            <span class="suffix">{{Suffix}}</span>
            */
        })),
        Get: function(Index)
        {
            var Records = [];
            this.each(function(Index, Ele)
            {
                Records.push({ Type: "QComboTree", Field: jQuery(Ele).data("options").Field, Value: jQuery(Ele).find("input").combotree((jQuery(Ele).data("options").Multiple == true || jQuery(Ele).data("options").Multiple == "true") ? "getValues" : "getValue") });
            });
            if(jQuery.isNumeric(Index) && Index < Records.length && Index >= 0)
            {
                return Records[Index];
            }
            else
            {
                return Records;
            }
        },
        Set: function(Value)
        {
            this.each(function(Index, Ele)
            {
                jQuery(Ele).find("input.value").combotree(((jQuery(Ele).data("options").Multiple == true || jQuery(Ele).data("options").Multiple == "true") ? "setValues" : "setValue"), Value);
            });
        },
        Show: CommonShow,
        Hide: CommonHide,
        Enable: function()
        {
            this.each(function(Index, Ele)
            {
                jQuery(Ele).find("input.value").combotree("enable");
            });
        },
        Disable: function()
        {
            this.each(function(Index, Ele)
            {
                jQuery(Ele).find("input.value").combotree("disable");
            });
        }
    };

    jQuery.fn.extend(
	{
	    Quick: function()
	    {
	        var This = this;

	        This.each(function(Index, Ele)
	        {
	            Ele = jQuery(Ele);
	            if(QTypes[Ele.attr("_type")] && !jQuery(Ele).data("options"))
	            {//类型存在，且没有初始化过
	                jQuery(Ele)[jQuery(Ele).attr("_type")]({});
	            }
	        });

	        var Handler =
			{
			    Get: function(Index)
			    {
			        var Records = [];

			        Records = Records.concat(This.filter(".text").QText().Get());

			        Records = Records.concat(This.filter(".combox").QCombox().Get());

			        Records = Records.concat(This.filter(".datetime").QDatetime().Get());

			        Records = Records.concat(This.filter(".number").QNumber().Get());

			        Records = Records.concat(This.filter(".auto_complete").QAutoComplete().Get());

			        Records = Records.concat(This.filter(".number_range").QNumberRange().Get());

			        Records = Records.concat(This.filter(".datetime_range").QDatetimeRange().Get());

			        Records = Records.concat(This.filter(".checkbox").QCheckbox().Get());

			        Records = Records.concat(This.filter(".timepicker").QTimePicker().Get());

			        Records = Records.concat(This.filter(".combotree").QComboTree().Get());

			        if(jQuery.isNumeric(Index) && Index < Records.length && Index >= 0)
                    {
                        return Records[Index];
                    }
                    else
                    {
                        return Records;
                    }
			    }
			};
	        return Handler;
	    },
	    QText: function(Options)
	    {
	        var This = this;
	        if(Options)
	        {
	            This.each(function(Index, Ele)
	            {
	                var JE = jQuery(Ele).addClass("quick text");
	                JE.attr("qfield", Options.Field);

	                var Opts = GetOptions(QText.Options, JE, Options);

	                JE.html(QText.Template(Opts)).data("options", Opts);
	            });
	        }
	        var Handler =
			{
			    Defaults: QText.Options,
			    Get: function(Index)
			    {
			        return QText.Get.call(This, Index);
			    },
			    Set: function(Value)
			    {
			        QText.Set.call(This, Value);
			    },
			    Show: function()
			    {
			        QText.Show.call(This);
			    },
			    Hide: function()
			    {
			        QText.Hide.call(This);
			    },
			    Enable: function()
			    {
			        QText.Enable.call(This);
			    },
			    Disable: function()
			    {
			        QText.Disable.call(This);
			    }
			};
	        return Handler;
	    },
	    QCombox: function(Options)
	    {
	        var This = this;
	        if(Options)
	        {
	            This.each(function(Index, Ele)
	            {
	                var JE = jQuery(Ele).addClass("quick combox");
	                JE.attr("qfield", Options.Field);
	                var Opts = GetOptions(QCombox.Options, JE, Options);
	                JE.html(QCombox.Template(Opts)).data("options", Opts);

                    if(jQuery.isFunction(Opts.Formatter) == false)
                    {
	                    Opts.Formatter = function(Row)
	                    {
	                        if(Opts.Multiple)
	                        {
	                            return "<div class='combocheckbox'>" + Row[Opts.TextField] + "</div>";
	                        } 
                            else
	                        {
	                            return "<div>" + Row[Opts.TextField] + "</div>";
	                        }
	                    }
                    }
	                JE.find("input").combobox({
	                    valueField: Opts.ValueField,
	                    textField: Opts.TextField,
	                    data: Opts.Data,
	                    editable: (Opts.Editable == true || Opts.Editable == "true") ? true : false,
	                    width: Opts.Width,
	                    onSelect: Opts.OnSelect,
	                    formatter: Opts.Formatter,
	                    onLoadSuccess: Opts.OnLoadSuccess,
	                    width: Opts.Width,
	                    panelWidth: Opts.PanelWidth,
	                    height: Opts.Height,
	                    panelHeight: Opts.PanelHeight,
						multiple: Opts.Multiple,
					
	                });
                    
	                if(Opts.Value)
	                {
	                    if(Opts.Multiple)
	                    {
	                        jQuery(Ele).find("input.value").combobox("setValues", Opts.Value);
	                    }
                        else
	                    {
	                        jQuery(Ele).find("input.value").combobox("setValue", Opts.Value);
	                    }
					}else if(Opts.Required){
						if(Opts.Data.length>0){
							jQuery(Ele).find("input.value").combobox("setValue", Opts.Data[0][Opts.ValueField]);
						}
					}
					
	            });
	        }
	        var Handler =
            {
                Defaults: QCombox.Options,
                Get: function(Index)
                {
                    return QCombox.Get.call(This, Index);
                },
                Set: function(Value)
                {
                    QCombox.Set.call(This, Value);
                },
                Show: function()
                {
                    QCombox.Show.call(This);
                },
                Hide: function()
                {
                    QCombox.Hide.call(This);
                },
                Enable: function()
                {
                    QCombox.Enable.call(This);
                },
                Disable: function()
                {
                    QCombox.Disable.call(This);
                }
            };
	        return Handler;
	    },
	    QAutoComplete: function(Options)
	    {
	        var This = this;
	        if(Options)
	        {
	            This.each(function(Index, Ele)
	            {
	                var JE = jQuery(Ele).addClass("quick auto_complete");
	                JE.attr("qfield", Options.Field);

	                var Opts = GetOptions(QAutoComplete.Options, JE, Options);

	                JE.html(QAutoComplete.Template(Opts)).data("options", Opts);

	                JE.find("input").autocomplete(Opts.Data,
                    {
                        max: Opts.Max,
                        minChars: Opts.MinChars,
                        matchCase: Opts.MatchCase,
                        matchContains: Opts.MatchContains,
                        autoFill: Opts.AutoFill,
                        scroll: Opts.Scroll,
                        mustMatch: Opts.MustMatch,
                        formatItem: Opts.OnFormatItem,
                        formatMatch: Opts.OnFormatMatch,
                        formatResult: Opts.OnFormatResult
                    }).result(Opts.OnCallback);
	            });
	        }

	        var Handler =
            {
                Defaults: QAutoComplete.Options,
                Get: function(Index)
                {
                    return QAutoComplete.Get.call(This, Index);
                },
                Set: function(Value)
                {
                    QAutoComplete.Set.call(This, Value);
                },
                Show: function()
                {
                    QAutoComplete.Show.call(This);
                },
                Hide: function()
                {
                    QAutoComplete.Hide.call(This);
                },
                Enable: function()
                {
                    QAutoComplete.Enable.call(This);
                },
                Disable: function()
                {
                    QAutoComplete.Disable.call(This);
                }
            };

	        return Handler;
	    },
	    QDatetime: function(Options)
	    {
	        var This = this;
	        if(Options)
	        {
	            This.each(function(Index, Ele)
	            {
	                var JE = jQuery(Ele).addClass("quick datetime");
	                JE.attr("qfield", Options.Field);

	                var Opts = GetOptions(QDatetime.Options, JE, Options);

	                JE.html(QDatetime.Template(Opts)).data("options", Opts).find("div.operator>div").click(function(Evt)
	                {
	                    if(jQuery(this).attr("disabled") != "disabled")
	                    {
	                        var Ipt = jQuery(this).parents(".quick").find("input.value");
	                        var Crt = ConvertToDate(Ipt.val(), Opts.Format);
	                        var Offset = -1;
	                        if(jQuery(this).hasClass("prev"))
	                        {
	                            Offset = 1;
	                        }
	                        switch(GetDateType(Opts.Format).split("").reverse()[0])
	                        {
	                            case "y":
	                                {
	                                    Crt = Crt.AddYears(Offset);
	                                }
	                                break;
	                            case "M":
	                                {
	                                    Crt = Crt.AddMonths(Offset);
	                                }
	                                break;
	                            case "d":
	                                {
	                                    Crt = Crt.AddDays(Offset);
	                                }
	                                break;
	                            case "H":
	                                {
	                                    Crt = Crt.AddHours(Offset);
	                                }
	                                break;
	                            case "m":
	                            case "s":
	                                {
	                                    Crt = Crt.AddMinutes(Offset);
	                                }
	                                break;
	                        }
	                        Ipt.val(Crt.FormatString(Opts.Format));
	                        if(Opts.OnChange)
	                        {
	                            Opts.OnChange.call(Ipt);
	                        }
	                    }
	                });
	            });
	        }
	        var Handler =
            {
                Defaults: QDatetime.Options,
                Get: function(Index)
                {
                    return QDatetime.Get.call(This, Index);
                },
                Set: function(Value)
                {
                    QDatetime.Set.call(This, Value);
                },
                Show: function()
                {
                    QDatetime.Show.call(This);
                },
                Hide: function()
                {
                    QDatetime.Hide.call(This);
                },
                Enable: function()
                {
                    QDatetime.Enable.call(This);
                },
                Disable: function()
                {
                    QDatetime.Disable.call(This);
                }
            };
	        return Handler;
	    },
	    QTimePicker: function(Options)
	    {
	        var This = this;
	        if(Options)
	        {
	            This.each(function(Index, Ele)
	            {
	                var JE = jQuery(Ele).addClass("quick timepicker");
	                JE.attr("qfield", Options.Field);

	                var Opts = GetOptions(QTimePicker.Options, JE, Options);

	                JE.html(QTimePicker.Template(Opts)).data("options", Opts).find("div.operator>div").click(function(Evt)
	                {
	                    if(jQuery(this).attr("disabled") != "disabled")
	                    {
	                        var Crt = JE.find("input.current");
	                        if(Crt.length == 0)
	                        {
	                            Crt = JE.find("input.hh");
	                        }
	                        var Val = Number(Crt.val()) || 0;
	                        if(jQuery(this).hasClass("prev"))
	                        {
	                            Val += 1;
	                        }
	                        else
	                        {
	                            Val -= 1;
	                        }
	                        if(Crt.hasClass("hh"))
	                        {
	                            if(Val < 0)
	                            {
	                                Val = 23;
	                            }
	                            else
	                            {
	                                Val %= 24;
	                            }
	                        }
	                        else
	                        {
	                            if(Val < 0)
	                            {
	                                Val = 59;
	                            }
	                            else
	                            {
	                                Val %= 60;
	                            }
	                        }
	                        Crt.val((Val < 10 ? "0" : "") + Val).click();
	                    }
	                });

	                JE.find("span.input>input").focusout(function(Evt)
	                {
	                    if(jQuery(this).val() == "")
	                    {
	                        jQuery(this).val("00");
	                    }
	                }).click(function(Evt)
	                {
	                    var This = this;
	                    JE.find("span.input>input").removeClass("current");
	                    jQuery(this).addClass("current");
	                    setTimeout(function() { jQuery(This).select(); }, 30);
	                }).keydown(function(Evt)
	                {
	                    var Crt = jQuery(this).val();
	                    var Wch = Evt.which;

	                    if(Wch == 186 || Wch == 110 || Wch == 39)//: . →
	                    {
	                        if(jQuery(this).hasClass("hh"))
	                        {
	                            if(Crt.length == 0)
	                            {
	                                JE.find("input.hh").val("00");
	                            }
	                            else if(Crt.length == 1)
	                            {
	                                JE.find("input.hh").val("0" + Crt);
	                            }
	                            else
	                            {
	                                JE.find("input.hh").val(Crt);
	                            }
	                        }
	                        else
	                        {
	                            if(Crt.length == 0)
	                            {
	                                JE.find("input.mm").val("00");
	                            }
	                            else if(Crt.length == 1)
	                            {
	                                JE.find("input.mm").val("0" + Crt);
	                            }
	                            else
	                            {
	                                JE.find("input.mm").val(Crt);
	                            }
	                        }
	                        JE.find("input.mm").click();
	                        return false;
	                    }
	                    else if(Wch == 37)//←
	                    {
	                        if(Crt.length == 0)
	                        {
	                            JE.find("input.mm").val("00");
	                        }
	                        else if(Crt.length == 1)
	                        {
	                            JE.find("input.mm").val("0" + Crt);
	                        }
	                        else
	                        {
	                            JE.find("input.mm").val(Crt);
	                        }
	                        JE.find("input.hh").click();
	                        return false;
	                    }
	                    else if(Wch == 13)
	                    {
	                        if(jQuery(this).hasClass("hh"))
	                        {
	                            JE.find("input.hh").val((Crt.length == 2 ? "" : "0") + Crt);
	                        }
	                        else
	                        {
	                            JE.find("input.mm").val((Crt.length == 2 ? "" : "0") + Crt);
	                        }
	                        JE.find("input.mm").click();
	                        return false;
	                    }
	                    else if(Wch > 47 && Wch < 58)
	                    {
	                        if(Crt.length == 2)
	                        {
	                            Crt = "";
	                        }
	                        if(jQuery(this).hasClass("hh"))
	                        {
	                            switch(Crt)
	                            {
	                                case "":
	                                    {
	                                        if(Wch > 50)
	                                        {
	                                            JE.find("input.hh").val("0" + (Wch - 48));
	                                            JE.find("input.mm").focus().click();
	                                        }
	                                    }
	                                    break;
	                                case "0":
	                                case "1":
	                                    {
	                                        JE.find("input.hh").val(Crt + (Wch - 48));
	                                        JE.find("input.mm").click();
	                                    }
	                                    break;
	                                case "2":
	                                    {
	                                        if(Wch < 52)
	                                        {
	                                            JE.find("input.hh").val(Crt + (Wch - 48));
	                                        }
	                                        else
	                                        {
	                                            JE.find("input.hh").val("23");
	                                        }
	                                        JE.find("input.mm").click();
	                                    }
	                                    break;
	                                default:
	                                    {
	                                        JE.find("input.mm").click();
	                                    }
	                                    break;
	                            }
	                        }
	                        else
	                        {
	                            if(Crt == "" && Wch > 53)
	                            {
	                                JE.find("input.mm").val("0" + (Wch - 48));
	                            }
	                        }
	                    }
	                    else if(Wch > 95 && Wch < 106)
	                    {
	                        if(Crt.length == 2)
	                        {
	                            Crt = "";
	                        }
	                        if(jQuery(this).hasClass("hh"))
	                        {
	                            switch(Crt)
	                            {
	                                case "":
	                                    {
	                                        if(Wch > 98)
	                                        {
	                                            JE.find("input.hh").val("0" + (Wch - 96));
	                                            JE.find("input.mm").focus().click();
	                                        }
	                                    }
	                                    break;
	                                case "0":
	                                case "1":
	                                    {
	                                        JE.find("input.hh").val(Crt + (Wch - 96));
	                                        JE.find("input.mm").click();
	                                    }
	                                    break;
	                                case "2":
	                                    {
	                                        if(Wch < 100)
	                                        {
	                                            JE.find("input.hh").val(Crt + (Wch - 96));
	                                        }
	                                        else
	                                        {
	                                            JE.find("input.hh").val("23");
	                                        }
	                                        JE.find("input.mm").click();
	                                    }
	                                    break;
	                                default:
	                                    {
	                                        JE.find("input.mm").click();
	                                    }
	                                    break;
	                            }
	                        }
	                        else
	                        {
	                            if(Crt == "" && Wch > 101)
	                            {
	                                JE.find("input.mm").val("0" + (Wch - 96));
	                            }
	                        }
	                    }
	                    else
	                    {
	                        return false;
	                    }
	                });
	            });
	        }
	        var Handler =
            {
                Defaults: QTimePicker.Options,
                Get: function(Index)
                {
                    return QTimePicker.Get.call(This, Index);
                },
                Set: function(Value)
                {
                    QTimePicker.Set.call(This, Value);
                },
                Show: function()
                {
                    QTimePicker.Show.call(This);
                },
                Hide: function()
                {
                    QTimePicker.Hide.call(This);
                },
                Enable: function()
                {
                    QTimePicker.Enable.call(This);
                },
                Disable: function()
                {
                    QTimePicker.Disable.call(This);
                }
            };
	        return Handler;
	    },
	    QNumber: function(Options)
	    {
	        var This = this;
	        if(Options)
	        {
	            This.each(function(Index, Ele)
	            {
	                var JE = jQuery(Ele).addClass("quick number");
	                JE.attr("qfield", Options.Field);

	                var Opts = GetOptions(QNumber.Options, JE, Options);

	                JE.html(QNumber.Template(Opts)).data("options", Opts);
	            });
	        }
	        var Handler =
            {
                Defaults: QNumber.Options,
                Get: function(Index)
                {
                    return QNumber.Get.call(This, Index);
                },
                Set: function(Value)
                {
                    QNumber.Set.call(This, Value);
                },
                Show: function()
                {
                    QNumber.Show.call(This);
                },
                Hide: function()
                {
                    QNumber.Hide.call(This);
                },
                Enable: function()
                {
                    QNumber.Enable.call(This);
                },
                Disable: function()
                {
                    QNumber.Disable.call(This);
                }
            };
	        return Handler;
	    },
	    QNumberRange: function(Options)
	    {
	        var This = this;
	        if(Options)
	        {
	            This.each(function(Index, Ele)
	            {
	                var JE = jQuery(Ele).addClass("quick number_range");
	                JE.attr("qfield", Options.Field);

	                var Opts = GetOptions(QNumberRange.Options, JE, Options);

	                JE.html(QNumberRange.Template(Opts)).data("options", Opts);
	            });
	        }
	        var Handler =
            {
                Defaults: QNumberRange.Options,
                Get: function(Index)
                {
                    return QNumberRange.Get.call(This, Index);
                },
                Set: function(Min, Max)
                {
                    QNumberRange.Set.call(This, Min, Max);
                },
                Show: function()
                {
                    QNumberRange.Show.call(This);
                },
                Hide: function()
                {
                    QNumberRange.Hide.call(This);
                },
                Enable: function()
                {
                    QNumberRange.Enable.call(This);
                },
                Disable: function()
                {
                    QNumberRange.Disable.call(This);
                }
            };
	        return Handler;
	    },
	    QDatetimeRange: function(Options)
	    {
	        var This = this;
	        if(Options)
	        {
	            This.each(function(Index, Ele)
	            {
	                var JE = jQuery(Ele).addClass("quick datetime_range");
	                JE.attr("qfield", Options.Field);

	                var Opts = GetOptions(QDatetimeRange.Options, JE, Options);

                    if(!Opts.Id)
                    {
                        Opts.Id = new Date().getTime() + "_" + new Date().getMilliseconds();
                    }

	                JE.html(QDatetimeRange.Template(Opts)).data("options", Opts).find("div.operator>div").click(function(Evt)
	                {
	                    if(jQuery(this).attr("disabled") != "disabled")
	                    {
                            var IsBegin = jQuery(this).hasClass("v1");
	                        var Ipt = jQuery(this).parents(".quick").find("input.value" + (IsBegin ? ".v1" : ".v2"));
	                        var Crt = ConvertToDate(Ipt.val(), Opts.Format);
	                        var Offset = -1;
	                        if(jQuery(this).hasClass("prev"))
	                        {
	                            Offset = 1;
	                        }
	                        switch(GetDateType(Opts.Format).split("").reverse()[0])
	                        {
	                            case "y":
	                                {
	                                    Crt = Crt.AddYears(Offset);
	                                }
	                                break;
	                            case "M":
	                                {
	                                    Crt = Crt.AddMonths(Offset);
	                                }
	                                break;
	                            case "d":
	                                {
	                                    Crt = Crt.AddDays(Offset);
	                                }
	                                break;
	                            case "H":
	                                {
	                                    Crt = Crt.AddHours(Offset);
	                                }
	                                break;
	                            case "m":
	                            case "s":
	                                {
	                                    Crt = Crt.AddMinutes(Offset);
	                                }
	                                break;
	                        }
                            //判断是否满足前后大小顺序
                            var Other = ConvertToDate(jQuery(this).parents(".quick").find("input.value" + (IsBegin ? ".v2" : ".v1")).val(), Opts.Format);
                            if(IsBegin)
                            {
                                if(Crt <= Other)
                                {
                                    Ipt.val(Crt.FormatString(Opts.Format));
                                }
                            }
                            else
                            {
                                if(Crt >= Other)
                                {
	                                Ipt.val(Crt.FormatString(Opts.Format));
                                }
                            }
	                    }
	                });
	            });
	        }
	        var Handler =
            {
                Defaults: QDatetimeRange.Options,
                Get: function(Index)
                {
                    return QDatetimeRange.Get.call(This, Index);
                },
                Set: function(Begin, End)
                {
                    QDatetimeRange.Set.call(This, Begin, End);
                },
                Show: function()
                {
                    QDatetimeRange.Show.call(This);
                },
                Hide: function()
                {
                    QDatetimeRange.Hide.call(This);
                },
                Enable: function()
                {
                    QDatetimeRange.Enable.call(This);
                },
                Disable: function()
                {
                    QDatetimeRange.Disable.call(This);
                }
            };
	        return Handler;
	    },
	    QCheckbox: function(Options)
	    {
	        var This = this;
	        if(Options)
	        {
	            This.each(function(Index, Ele)
	            {
	                var JE = jQuery(Ele).addClass("quick checkbox");
	                JE.attr("qfield", Options.Field);

	                var Opts = GetOptions(QCheckbox.Options, JE, Options);

	                JE.html(QCheckbox.Template(Opts)).data("options", Opts);

	                if(Options.OnChange && jQuery.isFunction(Options.OnChange))
	                {
	                    JE.find("input[type=checkbox]").change(Options.OnChange);
	                }
	            });
	        }
	        var Handler =
            {
                Defaults: QCheckbox.Options,
                Get: function(Index)
                {
                    return QCheckbox.Get.call(This, Index);
                },
                Set: function(Value)
                {
                    QCheckbox.Set.call(This, Value);
                },
                Show: function()
                {
                    QCheckbox.Show.call(This);
                },
                Hide: function()
                {
                    QCheckbox.Hide.call(This);
                },
                Enable: function()
                {
                    QCheckbox.Enable.call(This);
                },
                Disable: function()
                {
                    QCheckbox.Disable.call(This);
                }
            };
	        return Handler;
	    },
	    QComboTree: function(Options)
	    {
	        var This = this;
	        if(Options)
	        {
	            This.each(function(Index, Ele)
	            {
	                var JE = jQuery(Ele).addClass("quick combotree");
	                JE.attr("qfield", Options.Field);
	                var Opts = GetOptions(QComboTree.Options, JE, Options);
	                JE.html(QComboTree.Template(Opts)).data("options", Opts);

	                JE.find("input").combotree({
	                    lines: true,
	                    checkbox: (Opts.ShowCheckbox == true || Opts.ShowCheckbox == "true") ? true : false,
	                    multiple: (Opts.Multiple == true || Opts.Multiple == "true") ? true : false,
	                    onlyLeafCheck: (Opts.OnlyLeafCheck == true || Opts.OnlyLeafCheck == "true") ? true : false,
	                    width: Opts.Width,
	                    height: Opts.Height,
	                    panelWidth: jQuery.isNumeric(Opts.PanelWidth) ? Number(Opts.PanelWidth) : null,
	                    panelHeight: jQuery.isNumeric(Opts.PanelHeight) ? Number(Opts.PanelHeight) : 200,
	                    data: Opts.Data,
	                    onClick: Opts.OnClick
	                });
	                if(Opts.Value)
	                {
	                    JE.find("input").combotree((Opts.Multiple ? "setValues" : "setValue"), Opts.Value);
	                }
	            });
	        }
	        var Handler =
            {
                Defaults: QComboTree.Options,
                Get: function(Index)
                {
                    return QComboTree.Get.call(This, Index);
                },
                Set: function(Value)
                {
                    QComboTree.Set.call(This, Value);
                },
                Show: function()
                {
                    QComboTree.Show.call(This);
                },
                Hide: function()
                {
                    QComboTree.Hide.call(This);
                },
                Enable: function()
                {
                    QComboTree.Enable.call(This);
                },
                Disable: function()
                {
                    QComboTree.Disable.call(This);
                }
            }
	        return Handler;
	    }
	});
})(jQuery);

QuickDateTimeChanged = function(Evt)
{
    jQuery(this).parents(".quick").data("options").OnChange.call(jQuery(this));
};