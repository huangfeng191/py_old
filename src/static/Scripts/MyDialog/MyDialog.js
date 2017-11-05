/*
* 新建：2012-08-08
* 人员：fox
* -----------------------------------
* 修改 ：2012-08-15
* 人员：fox
* 内容：兼容IE7
*
* 修改 ：2012-09-03
* 人员：fox
* 内容：修改阴影
*
* 修改 ：2012-09-04
* 人员：fox
* 内容：修改 取值对话框取值问题
*
* 修改 ：2012-11-01
* 人员：fox
* 内容：修改 对话框不指定尺寸时居中问题
*
* 修改 ：2012-12-03
* 人员：fox
* 内容：对话框按Key查询问题
*
* 修改 ：2012-12-12
* 人员：fox
* 内容：IE9.0兼容问题
* 
* 修改：2013-11-01
* 人员：fox
* 内容：点击确定按钮后验证出错，没有关闭对话框，在点击顶部关闭按钮时，返回值错误的问题。
* 
* 修改：2015-01-26
* 人员：fox
* 内容：增加自动关闭功能。
* 
* 修改：2015-03-26
* 人员：fox
* 内容：增加Content方式打开模态或非模态对话框功能。
* -----------------------------------
* 注意：文件夹及文件名称不能修改
* 测试浏览器：IE7、IE8
*/
if (!window.MyDialog)
{
    window.MyDialog =
        {
            Types:
                {
                    ModalDialog: "Modal",
                    ModelessDialog: "Modeless",
                    Confirm: "Confirm",
                    Message: "Message",
                    ValuePicker: "ValuePicker"
                },
            Icons:
                {
                    Error: "error",
                    Info: "info",
                    Question: "question",
                    Warning: "warning"
                },
            IdPreFix: "",
            IdCounter: 0,
            GetId: function ()
            {
                return window.MyDialog.IdPreFix + window.MyDialog.IdCounter++;
            },
            Dictionary:
                {

            },
            List: [],
            GetByKey: function (Key)
            {
                return window.MyDialog.Dictionary[Key];
            },
            Current: null,
            Arguments: null,
            ReturnValue: null,
            Position:
            {
                X: 0,
                Y: 0
            },
            MaxSize:
            {
                Width: jQuery(window).width() - 32,
                Height: jQuery(window).height() - 59
            }
        };

        jQuery.extend(
    {
        ImplantStyle: function (Module, Skin, Loaded)
        {
            var Config = jQuery(document).data(Module);
            if (!Config)
            {
                var Script = jQuery("script[src*='/" + Module + ".js']");
                if (Script.length == 0)
                {
                    Script = jQuery("script[src^='" + Module + ".js']");
                }
                var Regx = new RegExp(Module + "\.js.*$");
                var Path = Script.attr("src").replace(Regx, "");
                if (!Skin)
                {
                    Skin = Script.attr("skin") || "Default";
                }

                Config = { Skin: Skin, Path: Path };

                jQuery("<link href=\"" + Path + "Skins/" + Skin + "/skin.css\" rel=\"stylesheet\" type=\"text/css\" />").insertAfter(Script)
                .bind("load", function ()
                {
                    if (jQuery.isFunction(Loaded))
                    {
                        Loaded(Config);
                    }
                });


                jQuery(document).data(Module, Config);
            }
            return Config;
        }
    });

    //注入样式
    jQuery.ImplantStyle("MyDialog");

    /*显示对话框*/
    window.ShowDialog = function ShowMyDialog(Config, Arguments, Callback, Params)
    {
        var Obj = {};
        Obj.Id = window.MyDialog.GetId();
        Obj.Type = Config.Type || MyDialog.Types.ModalDialog;
        if (Obj.Type == window.MyDialog.Types.Confirm || Obj.Type == window.MyDialog.Types.Message)
        {
            Obj.Icon = Config.Icon ? Config.Icon : window.MyDialog.Icons.Info;
        }
        if (Config.Url)
        {
            Obj.Url = Config.Url;
        }
        if (Config.Content)
        {
            Obj.Content = Config.Content;
        }
        Obj.Message = Config.Message;
        Obj.Arguments = Arguments;
        Obj.Callback = Callback;
        Obj.Params = Params;
        Obj.AutoSize = Config.AutoSize == false ? false : true;
        Obj.Title = Config.Title ? Config.Title : "对话框";
        Obj.Help = Config.Help;
        Obj.Width = Config.Width ? Config.Width : 400;
        Obj.Height = Config.Height ? Config.Height : 300;
        Obj.Left = Config.Left ? Config.Left : 0;
        Obj.Top = Config.Top ? Config.Top : 0;
        Obj.IsCenter = Config.IsCenter == false ? false : true;
        Obj.ScrollEnabled = Config.ScrollEnabled ? true : false;
        Obj.CloseButton = Config.CloseButton == false ? false : true;
        Obj.AutoClose = Config.AutoClose || null;
        Obj.Show = MyDialog_Show;
        Obj.Close = MyDialog_Close;
        if (Config.Key)
        {
            Obj.Key = Config.Key;
            window.MyDialog.Dictionary[Config.Key] = Obj;
        }
        window.MyDialog.List.unshift(Obj);
        window.MyDialog.Current = Obj;
        //API
        window.MyDialog.Arguments = Obj.Arguments;
        window.MyDialog.Close = Obj.Close;
        window.MyDialog.Reset = MyDialog_Reset;

        //判断是否超出窗口高度
        if (Obj.Width > MyDialog.MaxSize.Width)
        {
            Obj.Width = MyDialog.MaxSize.Width;
        }

        if (Obj.Height > MyDialog.MaxSize.Height)
        {
            Obj.Height = MyDialog.MaxSize.Height;
        }

        Obj.Show();

        return Obj;
    };

    function MyDialog_Show()
    {
        /*蒙板*/
        var E_Mask = this.Element = document.createElement("div");
        document.body.appendChild(E_Mask);
        E_Mask.className = "my_dialog";
        E_Mask.onselectstart = MyDialog_Select;

        if (document.body.offsetHeight > document.documentElement.offsetHeight)
        {
            E_Mask.style.height = (document.body.offsetHeight - 4) + "px";
        }
        else
        {
            E_Mask.style.height = (document.documentElement.offsetHeight - 4) + "px";
        }

        if (document.body.offsetWidth > document.documentElement.offsetWidth)
        {
            E_Mask.style.width = (document.body.offsetWidth - 4) + "px";
        }
        else
        {
            E_Mask.style.width = (document.documentElement.offsetWidth - 4) + "px";
        }

        /*阴影*/
        var E_Body = document.createElement("div");
        E_Body.className = "my_body";
        E_Mask.appendChild(E_Body);

        /*边框*/
        var E_Border1 = document.createElement("div");
        E_Body.appendChild(E_Border1);

        var E_Border2 = document.createElement("div");
        E_Border1.appendChild(E_Border2);

        /*标题*/
        var E_Top = $("<div></div>");

        $(E_Border2).append(E_Top);
        E_Top.mousedown(MyDialog_MouseDown);

        var E_Title = $("<div class='title'></div>").html(this.Title).appendTo(E_Top);

        if (this.Help)
        {
            var Hm = this.Help;
            var E_Close = $("<a class='help' title=\"帮助\"></a>").appendTo(E_Top).click(function ()
            {
                ShowDialog({ Title: "帮助", Content: Hm });
            });
        }

        if (this.CloseButton)
        {
            var E_Close = $("<a class='close' title=\"关闭\"></a>").appendTo(E_Top).click(function ()
            {
                MyDialog_ButtonClose();
            });
        }

        var E_Border3 = $("<div class='body'></div>").appendTo($(E_Border2));
        var E_Border4 = $("<div></div>").appendTo($(E_Border3));

        if (this.Type == window.MyDialog.Types.ModalDialog || this.Type == window.MyDialog.Types.ModelessDialog)
        {
            if (this.Url)
            {
                var E_Border5 = $("<div></div>").appendTo(E_Border4);
                var E_Border6 = $("<div></div>").appendTo(E_Border5);
                var E_Border7 = $("<div></div>").appendTo(E_Border6);
                var Ifm = "<iframe id=\"" + this.Id + "_content\" allowtransparency=\"true\" allowfullscreen=\"true\" frameborder=\"0\" scrolling=\"";
                if (this.ScrollEnabled)
                {
                    Ifm += "auto";
                }
                else
                {
                    Ifm += "no";
                }
                Ifm += "\" onload=\"MyDialog_IframeLoad(this)\" width=\"";
                Ifm += this.Width + "\" height=\"" + this.Height + "\" ></iframe>";
                E_Border7.html(Ifm);
                this.Iframe = E_Border7.find("iframe")[0];
                E_Border7.find("iframe").width(this.Width).height(this.Height);
                this.Iframe.src = this.Url + (this.Url.indexOf("?") > 0 ? "&" : "?") + this.Id;
                this.CustomWindow = this.Iframe.contentWindow;
            }
            else if (this.Content)
            {
                var E_Border5 = $("<div></div>").appendTo(E_Border4);
                var E_Border6 = $("<div></div>").appendTo(E_Border5);
                var E_Border7 = $("<div></div>").appendTo(E_Border6);
                if (jQuery.isFunction(this.Content))
                {
                    this.Content.call(this, E_Border7, MyDialog.MaxSize);
                    E_Border7.css("max-width", MyDialog.MaxSize.Width).css("max-height", MyDialog.MaxSize.Height).css("overflow", "auto");
                }
                else
                {
                    E_Border7.css("max-width", MyDialog.MaxSize.Width).css("max-height", MyDialog.MaxSize.Height).css("overflow", "auto");
                    E_Border7.append(this.Content);
                }
                //E_Border7.width(this.Width).height(this.Height);
                this.Width = E_Border7.width();
                this.Height = E_Border7.height();
            }
        }
        else
        {
            var E_Content = $("<table></table>").appendTo(E_Border4);

            if (this.Type == window.MyDialog.Types.ValuePicker)
            {
                var Labels = this.Message.join ? this.Message : [this.Message];
                var Values = [];
                if (this.Arguments)
                {
                    Values = this.Arguments.join ? this.Arguments : [this.Arguments];
                }
                for (var i = 0, len = Labels.length; i < len; i++)
                {
                    var E_Row1 = $("<tr></tr>").appendTo(E_Content);
                    var E_Td3 = $("<td></td>").appendTo(E_Row1).html(Labels[i]);
                    var E_Td4 = $("<td></td>").appendTo(E_Row1).append("<input type='text' value='" + (Values[i] ? Values[i] : "") + "'></input>");
                }
            }
            else
            {
                var E_Row1 = $("<tr></tr>").appendTo(E_Content);
                var E_Td3 = $("<td class='icon'></td>").appendTo(E_Row1);
                var E_Icon = $("<div></div>").appendTo(E_Td3);
                E_Icon.addClass("icon_" + this.Icon);
                var E_Td4 = $("<td></td>").appendTo(E_Row1);
                E_Td4.html(this.Message.join ? this.Message.join("<br/>") : this.Message);
            }

            var E_Row2 = $("<tr></tr>").appendTo(E_Content);
            var E_Td5 = $("<td colspan=2></td>").appendTo(E_Row2);
            var E_Buttons = $("<div class='button'></div>").appendTo(E_Td5);
            if (this.Type == window.MyDialog.Types.Confirm || this.Type == window.MyDialog.Types.ValuePicker)
            {
                var E_Cancel = $("<input type=\"button\" class=\"btn btn_common right\" value=\"取消\" />").appendTo(E_Buttons);
                E_Cancel[0].onclick = MyDialog_Cancel;
            }
            var E_Confirm = $("<input type=\"button\" class=\"btn btn_confirm right\" value=\"确定\" />").appendTo(E_Buttons);
            E_Confirm[0].onclick = MyDialog_Confirm;

            if (E_Content[0].offsetWidth < 160)
            {
                this.Width = 160;
            }
            else
            {
                this.Width = 8 + E_Content[0].offsetWidth;
            }
            //E_Top.width(this.Width);
            this.Height = E_Body.offsetHeight;
        }

        if (this.IsCenter)
        {
            E_Body.style.left = this.Left = Number(MyDialog.MaxSize.Width - this.Width) / 2 + $(window).scrollLeft() + "px";
            E_Body.style.top = this.Top = Number(MyDialog.MaxSize.Height - this.Height) / 2 + $(window).scrollTop() + "px";
        }
        else
        {
            E_Body.style.left = this.Left + $(window).scrollLeft() + "px";
            E_Body.style.top = this.Top + $(window).scrollTop() + "px";
        }

        if (this.AutoClose)
        {
            var Seconds = this.AutoClose;
            var Title = this.Title;
            var Dlg = this;
            E_Title.html(this.Title + "(" + Seconds-- + "后关闭)");

            this.Timer = setInterval(function ()
            {
                if (Seconds == 0)
                {
                    Dlg.Close();
                }
                else
                {
                    E_Title.html(Title + "(" + Seconds-- + "后关闭)");
                }
            }, 1000);
        }

        //移除当前按钮的焦点，避免按钮被enter触发
        jQuery(document.activeElement).blur();
    };

    function MyDialog_IframeLoad(Win)
    {
        if (Win && Win.contentWindow)
        {
            Win.contentWindow.ShowDialog = window.ShowDialog;
            Win.contentWindow.MyDialog = window.MyDialog;
            if (window.MyDialog.List.length > 0 && window.MyDialog.List[0].AutoSize)
            {
                window.MyDialog.Reset({ Width: Win.contentWindow.offsetWidth, Height: Win.contentWindow.offsetHeight });
            }
            if (Win.contentWindow.Load)
            {
                Win.contentWindow.Load(window.MyDialog.Arguments);
            }
        }
    };

    /*页面元素不可以选择*/
    function MyDialog_Select()
    {
        if (event && event.srcElement && event.srcElement.tagName && event.srcElement.tagName.toLowerCase() != "input")
        {
            return false;
        }
    };

    function MyDialog_ButtonClose()
    {
        window.MyDialog.ReturnValue = null;
        MyDialog_Close();
    };

    function MyDialog_Close()
    {
        //当前窗口退出堆栈
        var Dlg = window.MyDialog.List.shift();
        if (Dlg.Timer)
        {
            clearInterval(Dlg.Timer);
        }
        if (window.MyDialog.List.length > 0) //堆栈中还存在对话框
        {
            //设置对话框接口属性为堆栈顶的对话框的属性
            window.MyDialog.Arguments = window.MyDialog.List[0].Arguments;
            window.MyDialog.Close = window.MyDialog.List[0].Close;
            window.MyDialog.Resize = window.MyDialog.List[0].Resize;
            window.MyDialog.Current = window.MyDialog.List[0];
        }
        //如果有卸载事件，执行
        if (Dlg.CustomWindow && Dlg.CustomWindow.Dispose)
        {
            Dlg.CustomWindow.Dispose();
        }
        //移除关闭对话框的元素
        Dlg.CustomWindow = null;
        if (Dlg.Iframe)
        {
            Dlg.Iframe.src = "";
            Dlg.Iframe = null;
        }
        $(Dlg.Element).remove();
        Dlg.Element = null;
        if (Dlg.Key)
        {
            delete window.MyDialog.Dictionary[Dlg.Key];
        }
        //如果有回调函数，则把返回参数作为回调参数执行回调函数
        if (Dlg.Callback != null)
        {
            Dlg.Callback(window.MyDialog.ReturnValue, Dlg.Params);
            window.MyDialog.ReturnValue = null;
        }
        Dlg = null;
    };

    function MyDialog_Reset(Options)
    {
        var Dlg = this.Current;
        if (jQuery.isNumeric(Options.Width) && Options.Width >= 0)
        {
            Dlg.Width = Options.Width;
        }
        if (jQuery.isNumeric(Options.Height) && Options.Height >= 0)
        {
            Dlg.Height = Options.Height;
        }
        jQuery(Dlg.Iframe).width(Dlg.Width).height(Dlg.Height);

        if (jQuery.isNumeric(Options.Left))
        {
            Dlg.Left = Options.Left;
        }
        if (jQuery.isNumeric(Options.Top))
        {
            Dlg.Top = Options.Top;
        }
        jQuery(Dlg.Element).find("div.my_body").css("left", Dlg.Left).css("top", Dlg.Top);
    };

    /*非客户对话框确定和取消按钮事件*/
    function MyDialog_Confirm()
    {
        if (window.MyDialog.Current.Type == window.MyDialog.Types.ValuePicker)
        {
            var Rtn = [];
            var Rows = this.parentElement.parentElement.parentElement.parentElement.rows;
            for (var i = 0, len = Rows.length - 1; i < len; i++)
            {
                Rtn.push(Rows[i].cells[1].children[0].value);
            }
            window.MyDialog.ReturnValue = Rtn;
        }
        else
        {
            window.MyDialog.ReturnValue = true;
        }
        window.MyDialog.Close();
    };

    function MyDialog_Cancel()
    {
        window.MyDialog.ReturnValue = false;
        window.MyDialog.Close();
    };

    /*对话框移动*/
    function MyDialog_MouseDown(event)
    {
        if ($(event.srcElement).hasClass("close"))
        {
            MyDialog_Close();
        }
        else
        {
            window.MyDialog.Position.X = event.clientX - jQuery(this).parents(".my_body").offset().left;
            window.MyDialog.Position.Y = event.clientY - jQuery(this).parents(".my_body").offset().top;

            jQuery(this).parents(".my_dialog").mousemove(MyDialog_MouseMove).mouseup(MyDialog_MouseUp);
        }
    };

    function MyDialog_MouseMove(Evt)
    {
        if (Evt.clientX > window.MyDialog.Position.X)
        {
            jQuery(this).find(".my_body").css("left", Evt.clientX - window.MyDialog.Position.X);
            MyDialog.Current.Left = Evt.clientX - window.MyDialog.Position.X;
        }
        if (Evt.clientY > window.MyDialog.Position.Y)
        {
            jQuery(this).find(".my_body").css("top", Evt.clientY - window.MyDialog.Position.Y);
            MyDialog.Current.Top = Evt.clientY - window.MyDialog.Position.Y;
        }
    };

    function MyDialog_MouseUp(Evt)
    {
        jQuery(this).unbind("mousemove").unbind("mouseup");
    };
};