//jQuery.ImplantStyle("Order", "Default");
jQuery.extend(
{
    OrderManage: function(Container, Options)
    {
        var Cmp = jQuery(Container).data("component");

        var CreateField = function()
        {
            var Selected = {};
            for(var i = 0, Arr = List.find("div.condition"), len = Arr.length; i < len; i++)
            {
                Selected[jQuery(Arr[i]).data("order").Field] = true;
            }
            var Fields = [];
            for(var i = 0, Arr = Cmp.Fields, len = Arr.length; i < len; i++)
            {
                if(!Selected[Arr[i].Field])
                {
                    Fields.push({ Field: Arr[i].Field, Name: Arr[i].Name });
                }
            }

            if(Fields.length > 0)
            {
                Fields[0].selected = true;
            }

            Layout.find("input[field=field]").combobox({ valueField: 'Field', textField: 'Name', data: Fields, editable: false });
        };

        if(!Cmp)
        {
            Cmp =
			{
			    Container: jQuery(Container),
			    Options: Options,
			    Orders: (Options.Orders ? Options.Orders : []),
			    Field: {},
			    Fields: Options.Fields,
			    Template: template.compile(jQuery.GetTemplate(function()
			    {
			        /*
			        <div class="condition">
			        <span class="width30" col="number">{{Number}}</span>

			        <span class="width200" col="field">{{Field}}</span>

			        <span class="width100" col="order">{{Type}}</span>

			        <span class="delete width60" col="delete">删除</span>
			        </div>
			        */
			    })),
			    //获取条件列表并返回
			    Get: function()
			    {
			        var Items = [];
			        for(var i = 0, Arr = this.Container.find("div.content>div.condition"), len = Arr.length; i < len; i++)
			        {
			            Items.push(jQuery(Arr[i]).data("order"));
			        }
			        return Items;
			    }
			};
            Cmp.Container.addClass("order_framework");

            //生成字段索引
            for(var i = 0, Arr = Cmp.Fields, len = Arr.length, All = Cmp.Field; i < len; i++)
            {
                All[Arr[i].Field] = Arr[i];
            }

            //生成布局元素
            var Layout = jQuery(jQuery.GetTemplate(function()
            {
                /*
                <div class="search_box">
                <span class="left" style="line-height:26px;height:26px;">排序字段：</span>
                <span class="left">
                <input class="left" field="field" style="line-height:26px;height:26px;"/>
                </span>
                <span class="left" style="line-height:26px;height:26px;margin:0 0 0 8px">排序方式：</span>
                <span class="left">
                <input class="left" field="order" style="width: 60px;line-height:26px;height:26px;" />
                </span>
                <a command="add" group='button' href='#' class='btn btn_common'><span class='icons icon_add'></span>增加</a>
                <a command="clear" group='button' href='#' class='btn btn_common'><span class='icons icon_del'></span>清空</a>
                </div>

                <div class="title">
                <span class="width30">序号</span>
                <span class="width200">字段</span>
                <span class="width100">排序</span>
                <span class="width60">操作</span>
                </div>

                <div class="content">
                </div>
                */
            })).appendTo(Container);

            var List = Cmp.Container.find("div.content");

            CreateField();

            Layout.find("input[field=order]").combobox({ valueField: 'Value', textField: 'Name', data: [{ Value: "false", Name: "升序", "selected": true }, { Value: "true", Name: "降序"}], editable: false });

            Layout.find("a[command=add]").click(function(Evt)
            {
                var Field = Layout.find("input[field=field]").combobox("getValue");
                if(Field)
                {
                    var Order = { Field: Field, Type: Layout.find("input[field=order]").combobox("getValue") == "true" ? true : false };
                    var Obj = { Field: Cmp.Field[Field].Name, Type: (Order.Type == true ? "降序" : "升序"), Number: (List.find("div.condition").length + 1) };
                    jQuery(Cmp.Template(Obj)).appendTo(List).data("order", Order).find("span[col=delete]").click(function(Evt)
                    {
                        jQuery(this).parents("div.condition").remove();
                        List.find("div.condition>span[col=number]").each(function(i, ele)
                        {
                            jQuery(ele).html(i + 1);
                        });
                        CreateField();
                    });

                    CreateField();
                }
            });

            Layout.find("a[command=clear]").click(function(Evt)
            {
                List.html("");
                CreateField();
            });

            if(Cmp.Orders && Cmp.Orders.length > 0)
            {
                for(var i = 0, Arr = Cmp.Orders, len = Arr.length; i < len; i++)
                {
                    var Order = Arr[i];
                    if(Cmp.Field[Order.Field])
                    {
                        var Obj = { Field: Cmp.Field[Order.Field].Name, Type: (Order.Type == true ? "降序" : "升序"), Number: (i + 1) };
                        jQuery(Cmp.Template(Obj)).appendTo(List).data("order", Order).find("span[col=delete]").click(function(Evt)
                        {
                            jQuery(this).parents("div.condition").remove();
                            List.find("div.condition>span[col=number]").each(function(i, ele)
                            {
                                jQuery(ele).html(i + 1);
                            });
                            CreateField();
                        });
                    }
                }
                CreateField();
            }

            //设置条件列表容器最大高度
            List.css("max-height", Cmp.Container.height() - Cmp.Container.find("div:first").outerHeight(true) - Cmp.Container.find("div:eq(1)").outerHeight(true));

            jQuery(Container).data("component", Cmp);
        }
        return Cmp;
    }
});
jQuery.ImplantStyle("Order", "Default");
