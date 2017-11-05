;jQuery.extend(
{
    Grid: function(Container, Options)
    {
        var GetPosition = function()
        {
            return { Rows: Cmp.Layout.Rows, Cols: Cmp.Layout.Cols, Row: this.attr("_row"), Col: this.attr("_col") };
        };

        var Select = function()
        {
            Cmp.Container.find("div.container").removeClass("selected");
            jQuery(this).addClass("selected");
        };
        var Cmp = jQuery(Container).data("component");

        if(!Cmp)
        {
            Cmp =
			{
			    Template: template.compile(jQuery.GetTemplate(function()
			    {
			        /*
			        <table>
			        {{each Layout as r i}}
			        <tr>
			        {{each r as c j}}
			        <td rowspan="{{c.RowSpan}}" colspan="{{c.ColSpan}}">
			        <div class="container" _row="{{i}}" _col="{{j}}" style="width:{{c.Width}}px;height:{{c.Height}}px;">
			        </div>
			        </td>
			        {{/each}}
			        </tr>
			        {{/each}}
			        </table>
			        */
			    })),
			    Containers: [],
			    Render: function(Layout)
			    {
			        if(Layout)
			        {
			            Cmp.Layout = Layout;
			        }
			        else
			        {
			            Layout = Cmp.Layout;
			        }
			        var Def = null;
			        var Width = Cmp.Container.width();
			        var Height = Cmp.Container.height();

			        if(Layout.Rows && Layout.Cols)
			        {//m*n字符串格式
			            //行列布局
			            var H = Math.floor(Height / Layout.Rows - 12);
			            var W = Math.floor(Width / Layout.Cols - 12);
			            Def = [];

			            for(var i = 0, len = Layout.Rows; i < len; i++)
			            {
			                var Rows = [];
			                Def.push(Rows);
			                for(var j = 0, lenj = Layout.Cols; j < lenj; j++)
			                {
			                    Rows.push({ RowSpan: 1, ColSpan: 1, Width: W, Height: H });
			                }
			            }
			        }
			        else if(jQuery.isArray(Layout) && Layout.length > 0 && jQuery.isArray(Layout[0]) && Layout[0].length > 0)
			        {//数组定义方式，支持合并
			            Def = Layout;
			        }

			        if(Def)
			        {
			            Cmp.Container.html("");
			            var Ctns = Cmp.Containers = [];
			            jQuery(Cmp.Template({ Layout: Def })).appendTo(Cmp.Container).find("div.container").mousedown(function(Evt)
			            {
			                Cmp.Current = this;
			            }).mouseup(function(Evt)
			            {
			                if(Cmp.Current == this)
			                {
			                    Cmp.Container.find("div.container").removeClass("selected");
			                    jQuery(this).addClass("selected");
			                    if(jQuery.isFunction(Options.OnClick))
			                    {
			                        Options.OnClick(jQuery.extend(jQuery(this), { GetPosition: GetPosition, Select: Select }));
			                    }
			                }
			                Cmp.Current = null;
			            }).each(function(i, ele)
			            {
			                Ctns.push(jQuery.extend(jQuery(ele), { GetPosition: GetPosition, Select: Select }));
			            });
			        }
			    },
			    GetContainer: function(Row, Col)
			    {
			        var Ctn = Cmp.Container.find("div.container[_row=" + Row + "][_col=" + Col + "]");
			        return jQuery.extend(Ctn, { GetPosition: GetPosition, Select: Select });
			    }
			};

            //注入样式
            Cmp.Path = jQuery.ImplantStyle("Grid", (Options.Skin || "Default")).Path;

            Cmp.Container = jQuery(Container).addClass("grid_framework");

            jQuery(Container).data("component", Cmp);

            if(Options.Layout)
            {
                Cmp.Render(Options.Layout);
            }
        }

        return Cmp;
    }
});