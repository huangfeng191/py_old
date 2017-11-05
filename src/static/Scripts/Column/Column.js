//jQuery.ImplantStyle("Column", "Default");
jQuery.extend(
{
    Column: function(Container, Options)
    {
        var Cmp = jQuery(Container).data("component");

        if(!Cmp)
        {
            Cmp =
			{
			    Container: jQuery(Container),
			    Options: Options,
			    Template: template.compile(jQuery.GetTemplate(function()
			    {
			        /*
			        <div class="title">
			        <span class="width30">序号</span>
			        <span class="width200">列名</span>
			        <span class="width60"><span class="allcheck"><input type="checkbox"></span>是否显示</span>
			        </div>

			        <div class="content">
			        {{each Fields as tn i}}
			        <div class="condition">
			        <span class="width30" col="number">{{i + 1}}</span>
			        <span class="width200" col="field">{{tn.Name}}</span>
			        <span class="width60" col="show">
			        <input type="checkbox"{{if tn.Hidden != true}} checked="checked"{{/if}} 
			        {{if tn.Frozen == true}} disabled="disabled"{{/if}} /></span>
			        </div>
			        {{/each}}
			        </div>
			        */
			    })),
			    Fields: Options.Fields,
			    //获取条件列表并返回
			    Get: function()
			    {
			        var Columns = [];
			        for(var i = 0, Arr = this.Container.find("div.content>div.condition"), len = Arr.length; i < len; i++)
			        {
			            var Ele = jQuery(Arr[i]);
			            var Column = Ele.data("field");
			            Column.Hidden = (Ele.find("span[col=show]>input:checked").length > 0 ? false : true);
			            Columns.push(Column);
			        }
			        return Columns
			    }
			};
            Cmp.Container.addClass("column_framework");

            //初始化，生成表头，空条件列表和新增按钮
            jQuery(Cmp.Template(Options)).appendTo(Container).find("div.condition").each(function(i, ele)
            {
                jQuery(ele).data("field", Cmp.Fields[i]);
            });

            //绑定全选复选框事件
            Cmp.Container.find("div.title input[type=checkbox]").click(function(Evt)
            {
                var Checked = this.checked;
                Cmp.Container.find("div.content>div.condition>span>input[type=checkbox]").each(function(Index, Ele)
                {
                    if(!Ele.disabled)
                    {
                        Ele.checked = Checked;
                    }
                });
            });

            //设置全选框选中状态
            var Checked = Cmp.Container.find("div.content>div.condition>span>input[type=checkbox]:checked").length;
            var All = Cmp.Container.find("div.content>div.condition>span>input[type=checkbox]").length;
            var Disabled = Cmp.Container.find("div.content>div.condition>span>input[type=checkbox][disabled]").length;
            if(Checked == All)
            {
                //全部选中
                Cmp.Container.find("div.title input[type=checkbox]").attr("checked", "checked");
            }
            if(Disabled == Checked)
            {
                //全不选中
                Cmp.Container.find("div.title input[type=checkbox]").removeAttr("checked");
            }

            //绑定列复选框事件
            Cmp.Container.find("div.content>div.condition>span>input[type=checkbox]").click(function(Evt)
            {
                var Checked = Cmp.Container.find("div.content>div.condition>span>input[type=checkbox]:checked").length;
                var All = Cmp.Container.find("div.content>div.condition>span>input[type=checkbox]").length;
                var Disabled = Cmp.Container.find("div.content>div.condition>span>input[type=checkbox][disabled]").length;
                if(Checked == All)
                {
                    //全部选中
                    Cmp.Container.find("div.title input[type=checkbox]").attr("checked", "checked");
                }
                if(Disabled == Checked)
                {
                    //全不选中
                    Cmp.Container.find("div.title input[type=checkbox]").removeAttr("checked");
                }
            });

            //设置条件列表容器最大高度
            Cmp.Container.find("div.content").css("max-height", Cmp.Container.height() - Cmp.Container.find("div:first").outerHeight(true));

            jQuery(Container).data("component", Cmp);
        }
        return Cmp;
    }
});
jQuery.ImplantStyle("Column", "Default");