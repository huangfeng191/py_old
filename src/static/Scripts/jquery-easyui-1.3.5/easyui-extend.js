/*form获得表单信息*/
(function($){
    function validate(target){
        if($.fn.validatebox){
            var box = $(".validatebox-text", target);
            if(box.length){
                box.validatebox("validate");
                var $invalids = $(".validatebox-invalid", target);
                var messages = $.map($invalids, function(ele){
                    var options = $.data(ele, "validatebox").options;
                    var label = "<span style=\"color:red;\">" + options.label + "</span>";
                    var temp = $.data(ele, "validatebox").messages;
                    return $.map(temp, function(m){
                        return label + m;
                    });
                });
                if($invalids.length == 0){
                    return true;
                } else{
                    window.top.ShowDialog({
                        Title: "提示", Type: window.top.MyDialog.Types.Message, Icon: window.top.MyDialog.Icons.Info,
                        Message: messages.join("<br/>")
                    });
                    return false;
                }
            }
        }
        return true;
    }

    $.extend($.fn.form.methods, {
        getData: function(jq){
            var array = jq.serializeArray();
            var result = {};

            for(var i = 0; i < array.length; i++){
                var $e = jq.find("*[name='" + array[i].name + "']");
                var datatype;
                if($e.is(".combo-value")){
                    var combos = ["combobox", "combotree", "combogrid", "datetimebox", "datebox", "combo"],
                    $c = jq.find("[comboName='" + array[i].name + "']");
                    for(var c = 0; c < combos.length; c++){
                        if(!$c.hasClass(combos[c] + "-f")){
                            continue;
                        }
                        datatype = $c[combos[c]]("options").datatype;
                        break;
                    }
                }
                else{
                    datatype = $e.data("type");
                }
                datatype = datatype || "string?";
                var nullable = datatype.indexOf("?") > -1;
                nullable && (datatype = datatype.replace("?", ""));
                if(nullable && array[i].value == ""){
                    result[array[i].name] = null;
                    continue;
                }
                switch(datatype){
                    case "number":
                        result[array[i].name] = Number(array[i].value) || 0;
                        break;
                    case "bool":
                        result[array[i].name] = !!Number(array[i].value);
                        break;
                    default:
                        result[array[i].name] = array[i].value;
                        break;
                }
            }
            return result;
        },
        enable: function(jq){
            jq.find("*[name]").each(function(){
                if($(this).is(".combo-value")){
                    var combos = ["combobox", "combotree", "combogrid", "datetimebox", "datebox", "combo"],
                    $c = jq.find("[comboName='" + $(this).attr("name") + "']");
                    for(var c = 0; c < combos.length; c++){
                        if(!$c.hasClass(combos[c] + "-f")){
                            continue;
                        }
                        $c[combos[c]]("enable");
                        break;
                    }
                }
                else{
                    $(this).removeProp("disabled");
                }
            });
        },
        disable: function(jq){
            jq.find("*[name]").each(function(){
                if($(this).is(".combo-value")){
                    var combos = ["combobox", "combotree", "combogrid", "datetimebox", "datebox", "combo"],
                    $c = jq.find("[comboName='" + $(this).attr("name") + "']");
                    for(var c = 0; c < combos.length; c++){
                        if(!$c.hasClass(combos[c] + "-f")){
                            continue;
                        }
                        $c[combos[c]]("disable");
                        break;
                    }
                }
                else{
                    $(this).prop("disabled", true);
                }
            });
        },
        validate: function(jq){
            return validate(jq[0]);
        }
    });
})(jQuery);

//重构easyui validatebox，验证显示效果仿通用增删改查。
(function($){
    function init(target){
        $(target).addClass("validatebox-text");
    }

    function destroyBox(target){
        var data = $.data(target, "validatebox");
        //设置validating为false，以阻止当前正在对target做校验的事件处理程序。
        data.validating = false;
        //解绑事件，删除DOM。
        $(target).off().remove();

    }

    function validator(options, validType, value, messages){
        var result = /([a-zA-Z_]+)(.*)/.exec(validType);
        var rule = options.rules[result[1]];
        if(rule && value){
            var param = eval(result[2]);
            if(!rule["validator"](value, param)){
                var message = rule["message"];
                if(param){
                    for(var i = 0; i < param.length; i++){
                        message = message.replace(new RegExp("\\{" + i + "\\}", "g"), param[i]);
                    }
                }
                messages.push(options.invalidMessage || message);
            }
        }
    }

    function validate(target){
        var data = $.data(target, "validatebox");
        var options = data.options;
        var box = $(target);
        var value = $.trim(box.val());
        var messages = [];

        if(options.required && !value){
            messages.push(options.missingMessage);
        }
        if(options.validType){
            if(typeof options.validType == "string"){
                validator(options, options.validType, value, messages);
            } else{
                for(var i = 0; i < options.validType.length; i++){
                    validator(options, options.validType[i], value, messages);
                }
            }
        }
        if(messages.length == 0){
            box.removeClass("validatebox-invalid");
            $.data(target, "validatebox").messages = messages;
            return true;
        } else{
            box.addClass("validatebox-invalid");
            $.data(target, "validatebox").messages = messages;
            return false;
        }
    }

    $.fn.validatebox = function(options, param){
        //看到了吧，easyui是通过入参来判断是构造组建还是调用组建方法。
        if(typeof options == "string"){
            //如果options是字符串型，则调用validatebox对用户提供的接口方法。
            return $.fn.validatebox.methods[options](this, param);
        }
        //如果构造函数没有入参，则设置options为{}空对象。
        options = options || {};

        //this指向jq选择器返回DOM对象列表，用each方法逐个初始化每个DOM。
        return this.each(function(){
            //获取绑定在DOM上名为validatebox的全局对象。
            var state = $.data(this, "validatebox");
            if(state){
                //如果validatebox已被初始化过，则覆盖原有配置参数。
                $.extend(state.options, options);
            } else{
                //如果validatebox未被初始化过，则初始化validatebox组建。
                init(this);
                //绑定一个名为validatebox的对象到DOM上，
                //该对象只包含options属性，options属性的获取优先级规则为：
                //传入的options>属性转换器>默认值
                $.data(this, "validatebox", {
                    options: $.extend({}, $.fn.validatebox.defaults, $.fn.validatebox.parseOptions(this), options)
                });
            }
        });
    };

    $.fn.validatebox.methods = {
        destroy: function(jq){
            return jq.each(function(){
                destroyBox(this);
            });
        },
        validate: function(jq){
            return jq.each(function(){
                validate(this);
            });
        },
        isValid: function(jq){
            return validate(jq[0]);
        }
    };

    $.fn.validatebox.parseOptions = function(target){
        var t = $(target);
        return $.extend({}, $.parser.parseOptions(target, ["validType", "missingMessage", "invalidMessage"]), {
            required: (t.attr("required") ? true : undefined)
        });
    };

    //默认验证规则
    $.fn.validatebox.defaults = {
        required: false, validType: null, delay: 200, missingMessage: "为必填项", invalidMessage: null, novalidate: false,
        rules: {
            email: {
                validator: function(value){
                    return /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i.test(value);
                },
                message: "邮件地址无效"
            }, url: {
                validator: function(value){
                    return /^(https?|ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(value);
                },
                message: "URL地址无效"
            }, length: {
                validator: function(value, param){
                    var len = $.trim(value).length;
                    return len >= param[0] && len <= param[1];
                },
                message: "长度必须介于{0}和{1}之间"
            }, remote: {
                validator: function(value, param){
                    var data = {};
                    data[param[1]] = value;
                    var _2f = $.ajax({url: param[0], dataType: "json", data: data, async: false, cache: false, type: "post"}).responseText;
                    return _2f == "true";
                },
                message: "字段不正确"
            }
        }
    };

    /*表单验证扩展*/
    $.extend($.fn.validatebox.defaults.rules, {
        //整数
        integer: {
            validator: function(value){
                return /^(-?\d+)?$/.test($.trim(value));
            },
            message: "必须为有效整数"
        },
        //正整数
        integerPos: {
            validator: function(value){
                return /^([1-9]\d*)?$/.test($.trim(value));
            },
            message: "必须为有效正整数"
        },
        //非负整数
        integerNon: {
            validator: function(value){
                return /^(\d{1,})?$/.test($.trim(value));
            },
            message: "必须为有效非负整数"
        },
        //正数
        numberPos: {
            validator: function(value){
                return /^(\d*(\.\d*)?)?$/.test($.trim(value)) ? !!Number(value) : false;
            },
            message: "必须为有效正数"
        },
        //非负数
        numberNon: {
            validator: function(value){
                return /^(\d*\.?\d*)?$/.test($.trim(value));
            },
            message: "必须为有效非负数"
        },
        //有效的电话号码
        Phone: {
            validator: function(value){
                return /^((?:0?(13|15|17|18|14)[0-9][0-9]{8})|(?:([0-9]{3,4}\-)?[0-9]{6,8}))?$/.test($.trim(value));
            },
            message: "必须为有效的电话号码"
        },
        IP: {
            validator: function(value){
                return /^((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))?$/.test($.trim(value));
            },
            message: "必须为有效IP地址"
        }
    });
})(jQuery);

//汉化
(function($){
    if($.fn.pagination){
        $.fn.pagination.defaults.beforePageText = '第';
        $.fn.pagination.defaults.afterPageText = '共{pages}页';
        $.fn.pagination.defaults.displayMsg = '显示{from}到{to},共{total}记录';
    }
    if($.fn.datagrid){
        $.fn.datagrid.defaults.loadMsg = '正在处理，请稍待。。。';
    }
    if($.fn.treegrid && $.fn.datagrid){
        $.fn.treegrid.defaults.loadMsg = $.fn.datagrid.defaults.loadMsg;
    }
    if($.messager){
        $.messager.defaults.ok = '确定';
        $.messager.defaults.cancel = '取消';
    }
    if($.fn.numberbox){
        $.fn.numberbox.defaults.missingMessage = '为必填项';
    }
    if($.fn.combo){
        $.fn.combo.defaults.missingMessage = '为必填项';
    }
    if($.fn.combobox){
        $.fn.combobox.defaults.missingMessage = '为必填项';
    }
    if($.fn.combotree){
        $.fn.combotree.defaults.missingMessage = '为必填项';
    }
    if($.fn.combogrid){
        $.fn.combogrid.defaults.missingMessage = '为必填项';
    }
    if($.fn.calendar){
        $.fn.calendar.defaults.weeks = ['日', '一', '二', '三', '四', '五', '六'];
        $.fn.calendar.defaults.months = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];
    }
    if($.fn.datebox){
        $.fn.datebox.defaults.currentText = '今天';
        $.fn.datebox.defaults.closeText = '关闭';
        $.fn.datebox.defaults.okText = '确定';
        $.fn.datebox.defaults.missingMessage = '为必填项';
        $.fn.datebox.defaults.formatter = function(date){
            var y = date.getFullYear();
            var m = date.getMonth() + 1;
            var d = date.getDate();
            return y + '-' + (m < 10 ? ('0' + m) : m) + '-' + (d < 10 ? ('0' + d) : d);
        };
        $.fn.datebox.defaults.parser = function(s){
            if(!s){
                return new Date();
            }
            var ss = s.split('-');
            var y = parseInt(ss[0], 10);
            var m = parseInt(ss[1], 10);
            var d = parseInt(ss[2], 10);
            if(!isNaN(y) && !isNaN(m) && !isNaN(d)){
                return new Date(y, m - 1, d);
            } else{
                return new Date();
            }
        };
    }
    if($.fn.datetimebox && $.fn.datebox){
        $.extend($.fn.datetimebox.defaults, {
            currentText: $.fn.datebox.defaults.currentText,
            closeText: $.fn.datebox.defaults.closeText,
            okText: $.fn.datebox.defaults.okText,
            missingMessage: $.fn.datebox.defaults.missingMessage
        });
    }
})(jQuery);