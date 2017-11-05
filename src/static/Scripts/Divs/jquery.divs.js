!function (e) { "use strict"; var n = function (e, r) { return n["string" == typeof r ? "compile" : "render"].apply(n, arguments) }; n.version = "2.0.4", n.openTag = "<%", n.closeTag = "%>", n.isEscape = !0, n.isCompress = !1, n.parser = null, n.render = function (e, r) { var t = n.get(e) || a({ id: e, name: "Render Error", message: "No Template" }); return t(r) }, n.compile = function (e, t) { function o(r) { try { return new l(r, e) + "" } catch (i) { return s ? a(i)() : n.compile(e, t, !0)(r) } } var c = arguments, s = c[2], u = "anonymous"; "string" != typeof t && (s = c[1], t = c[0], e = u); try { var l = i(e, t, s) } catch (p) { return p.id = e || t, p.name = "Syntax Error", a(p) } return o.prototype = l.prototype, o.toString = function () { return l.toString() }, e !== u && (r[e] = o), o }; var r = n.cache = {}, t = n.helpers = function () { var e = function (n, r) { return "string" != typeof n && (r = typeof n, "number" === r ? n += "" : n = "function" === r ? e(n.call(n)) : ""), n }, r = { "<": "&#60;", ">": "&#62;", '"': "&#34;", "'": "&#39;", "&": "&#38;" }, t = function (n) { return e(n).replace(/&(?![\w#]+;)|[<>"']/g, function (e) { return r[e] }) }, a = Array.isArray || function (e) { return "[object Array]" === {}.toString.call(e) }, i = function (e, n) { if (a(e)) for (var r = 0, t = e.length; t > r; r++) n.call(e, e[r], r, e); else for (r in e) n.call(e, e[r], r) }; return { $include: n.render, $string: e, $escape: t, $each: i } }(); n.helper = function (e, n) { t[e] = n }, n.onerror = function (n) { var r = "Template Error\n\n"; for (var t in n) r += "<" + t + ">\n" + n[t] + "\n\n"; e.console && console.error(r) }, n.get = function (t) { var a; if (r.hasOwnProperty(t)) a = r[t]; else if ("document" in e) { var i = document.getElementById(t); if (i) { var o = i.value || i.innerHTML; a = n.compile(t, o.replace(/^\s*|\s*$/g, "")) } } return a }; var a = function (e) { return n.onerror(e), function () { return "{Template Error}" } }, i = function () { var e = t.$each, r = "break,case,catch,continue,debugger,default,delete,do,else,false,finally,for,function,if,in,instanceof,new,null,return,switch,this,throw,true,try,typeof,var,void,while,with,abstract,boolean,byte,char,class,const,double,enum,export,extends,final,float,goto,implements,import,int,interface,long,native,package,private,protected,public,short,static,super,synchronized,throws,transient,volatile,arguments,let,yield,undefined", a = /\/\*[\w\W]*?\*\/|\/\/[^\n]*\n|\/\/[^\n]*$|"(?:[^"\\]|\\[\w\W])*"|'(?:[^'\\]|\\[\w\W])*'|[\s\t\n]*\.[\s\t\n]*[$\w\.]+/g, i = /[^\w$]+/g, o = new RegExp(["\\b" + r.replace(/,/g, "\\b|\\b") + "\\b"].join("|"), "g"), c = /^\d[^,]*|,\d[^,]*/g, s = /^,+|,+$/g, u = function (e) { return e.replace(a, "").replace(i, ",").replace(o, "").replace(c, "").replace(s, "").split(/^$|,+/) }; return function (r, a, i) { function o(e) { return m += e.split(/\n/).length - 1, n.isCompress && (e = e.replace(/[\n\r\t\s]+/g, " ").replace(/<!--.*?-->/g, "")), e && (e = x[1] + p(e) + x[2] + "\n"), e } function c(e) { var r = m; if ($ ? e = $(e) : i && (e = e.replace(/\n/g, function () { return m++, "$line=" + m + ";" })), 0 === e.indexOf("=")) { var a = !/^=[=#]/.test(e); if (e = e.replace(/^=[=#]?|[\s;]*$/g, ""), a && n.isEscape) { var o = e.replace(/\s*\([^\)]+\)/, ""); t.hasOwnProperty(o) || /^(include|print)$/.test(o) || (e = "$escape(" + e + ")") } else e = "$string(" + e + ")"; e = x[1] + e + x[2] } return i && (e = "$line=" + r + ";" + e), s(e), e + "\n" } function s(n) { n = u(n), e(n, function (e) { e && !v.hasOwnProperty(e) && (l(e), v[e] = !0) }) } function l(e) { var n; "print" === e ? n = k : "include" === e ? (y.$include = t.$include, n = E) : (n = "$data." + e, t.hasOwnProperty(e) && (y[e] = t[e], n = 0 === e.indexOf("$") ? "$helpers." + e : n + "===undefined?$helpers." + e + ":" + n)), w += e + "=" + n + "," } function p(e) { return "'" + e.replace(/('|\\)/g, "\\$1").replace(/\r/g, "\\r").replace(/\n/g, "\\n") + "'" } var f = n.openTag, d = n.closeTag, $ = n.parser, g = a, h = "", m = 1, v = { $data: 1, $id: 1, $helpers: 1, $out: 1, $line: 1 }, y = {}, w = "var $helpers=this," + (i ? "$line=0," : ""), b = "".trim, x = b ? ["$out='';", "$out+=", ";", "$out"] : ["$out=[];", "$out.push(", ");", "$out.join('')"], T = b ? "$out+=$text;return $text;" : "$out.push($text);", k = "function($text){" + T + "}", E = "function(id,data){data=data||$data;var $text=$helpers.$include(id,data,$id);" + T + "}"; e(g.split(f), function (e) { e = e.split(d); var n = e[0], r = e[1]; 1 === e.length ? h += o(n) : (h += c(n), r && (h += o(r))) }), g = h, i && (g = "try{" + g + "}catch(e){" + "throw {" + "id:$id," + "name:'Render Error'," + "message:e.message," + "line:$line," + "source:" + p(a) + ".split(/\\n/)[$line-1].replace(/^[\\s\\t]+/,'')" + "};" + "}"), g = w + x[0] + g + "return new String(" + x[3] + ");"; try { var j = new Function("$data", "$id", g); return j.prototype = y, j } catch (O) { throw O.temp = "function anonymous($data,$id) {" + g + "}", O } } }(); "function" == typeof define ? define(function () { return n }) : "undefined" != typeof exports && (module.exports = n), e.template = n }(this), function (e) { e.openTag = "{{", e.closeTag = "}}", e.parser = function (n) { n = n.replace(/^\s/, ""); var r = n.split(" "), t = r.shift(), a = r.join(" "); switch (t) { case "if": n = "if(" + a + "){"; break; case "else": r = "if" === r.shift() ? " if(" + r.join(" ") + ")" : "", n = "}else" + r + "{"; break; case "/if": n = "}"; break; case "each": var i = r[0] || "$data", o = r[1] || "as", c = r[2] || "$value", s = r[3] || "$index", u = c + "," + s; "as" !== o && (i = "[]"), n = "$each(" + i + ",function(" + u + "){"; break; case "/each": n = "});"; break; case "echo": n = "print(" + a + ");"; break; case "include": n = "include(" + r.join(",") + ");"; break; default: e.helpers.hasOwnProperty(t) ? n = "=#" + t + "(" + r.join(",") + ");" : (n = n.replace(/[\s;]*$/, ""), n = "=" + n) } return n } }(this.template);
document.write("<script src='/static/gis/JS/template-simple.js' type='text/javascript'></script>");

(function($,h,c){var a=$([]),e=$.resize=$.extend($.resize,{}),i,k="setTimeout",j="resize",d=j+"-special-event",b="delay",f="throttleWindow";e[b]=250;e[f]=true;$.event.special[j]={setup:function(){if(!e[f]&&this[k]){return false}var l=$(this);a=a.add(l);$.data(this,d,{w:l.width(),h:l.height()});if(a.length===1){g()}},teardown:function(){if(!e[f]&&this[k]){return false}var l=$(this);a=a.not(l);l.removeData(d);if(!a.length){clearTimeout(i)}},add:function(l){if(!e[f]&&this[k]){return false}var n;function m(s,o,p){var q=$(this),r=$.data(this,d);r.w=o!==c?o:q.width();r.h=p!==c?p:q.height();n.apply(this,arguments)}if($.isFunction(l)){n=l;return m}else{n=l.handler;l.handler=m}}};function g(){i=h[k](function(){a.each(function(){var n=$(this),m=n.width(),l=n.height(),o=$.data(this,d);if(m!==o.w||l!==o.h){n.trigger(j,[o.w=m,o.h=l])}});g()},e[b])}})(jQuery,this);

$.fn.Divs = function(options)
{
    var target = this;

    var defaults = {
        data: { text: "所有站点", id: "0", children: [{ text: "111111", id: "1", children: [{ text: "432111", id: "3", children: []}] }, { text: "222222", id: "1", children: [] }, { text: "33333", id: "1", children: [] }, { text: "444444", id: "1", children: [] }, { text: "555555", id: "1", children: []}] },
        nameField: "text",
        idField: "id",
        childrenField: "children",
        showAll:true,
        titleName:"当前片区：",
        onClick: function(ele, type, ids)
        {

        }
    }
    
     template.helper("getMenu", function (val) {
    	 var html="";
    	 if(val.Children.length==0){
    		 return "<a href='#' data-id="+(val.ObjId)+"  class='hasConfig'>"+(val.Name)+"</a>";
    	 }else{
	    	return "<div class='four'>" +
			    	"<a href='#' data-id="+(val.ObjId)+"  class='hasConfig'>"+(val.Name)+"</a>" +
			    		"<div class='four-float-right'>" +
			    			"<div class='four-box'>" +
			    				"<div class='four-div' style='display:none' name="+(val.ObjId)+">" +
			    					"<div class='four-menu'>" +
			    						"<div class='four-menu-box'>" +
			    							"<div class='four-menu-box-detail'>" +
			    								"<ul>" +
			    									temp(val.Children) +
	    										"</ul>" +
    										"</div>" +
										"</div>" +
									"</div>" +
								"</div>" +
							"</div>" +
						"</div>" +
		    		"</div>";
    	}
    })
    function temp(val){
    	if(val==undefined){
    		return false;
    	}
    	var html="";
    	for(var i=0;i<val.length;i++){
    		html += tem(val[i]);
    	}
    	return html;
    }
    function tem(val){
    	var html="";
    	if(val.Children.length>0){
    		html = "<li>" +
	        	"<div class='four'>" +
	        	"<a href='#' data-id="+(val.ObjId)+"  class='hasConfig'>"+(val.Name)+"</a>" +
	        		"<div class='four-float-right'>" +
	        			"<div class='four-box'>" +
	        				"<div class='four-div' style='display:none' name="+(val.ObjId)+">" +
	        					"<div class='four-menu'>" +
	        						"<div class='four-menu-box'>" +
	        							"<div class='four-menu-box-detail'>" +
	        								"<ul>" +
	        									temp(val.Children) +
											"</ul>" +
										"</div>" +
									"</div>" +
								"</div>" +
							"</div>" +
						"</div>" +
	        		"</div>" +
	    		"</div>" +
    		"</li>";
    	}else{
    		html = "<li><a href='#' data-id="+(val.ObjId)+"  class='hasConfig'>"+(val.Name)+"</a></li>";
    	}
    	return html;
    }

    var divs = {
        _template: "\
          	<div class='area_divs' id='divs_control'>\
	         	<div class='area-left'></div>\
	         	<div class='area-right'></div>\
	         	<div class='area-mid'>\
		           	<div class='title'>titleName：<span class='thediv' >显示全部</span></div>\
		           	<a class='gis-icon icon-arrow-left prev' href='javascript:;'></a>\
		           	<a class='gis-icon icon-arrow-right next' href='javascript:;'></a>\
		           	<div class='area-content'>\
		               {{each children as value index}}\
		                   	<div class='area-root'>\
		                   		<a href='#' data-id='{{value.id}}' class='hasConfig' >{{value.name}}</a>\
		                        {{if value.children.length>0}}\
		                        <div class='sub' style='display:none'>\
		                        	<div class='sub-con'>\
		                        		<div class='sub-con-data'>\
		                        			<div class='sub-con-data-detail'>\
		                        				<ul>\
					                            {{each value.children as t index}}\
													<li>\
														<div class='three'>\
			                                                <a href='#' data-id='{{t.id}}'  class='hasConfig'>{{t.name}}</a>\
			                                                {{if t.children.length>0}}\
			                                                    <div class='float-right'>\
			                                                        <div class='three-box'>\
			                                                            <div class='three-div' style='display:none'>\
			        														<div class='three-menu'>\
											                             		<div class='three-menu-box'>\
											                        				<div class='three-menu-box-detail'>\
			                                                                    		<ul>\
						                                                        			{{each t.children as s index}}\
			                                                                            		<li>\
			                                                                            			{{getMenu s}}\
			                                                                            		</li>\
			        																		{{/each}}\
						                                                        		</ul>\
			                                                            			</div>\
			                                                       		  		</div>\
			                                                            	</div>\
			                                                        	</div>\
			                                                        </div>\
			                                                   </div>\
			                                                {{/if}}\
			                                              </div>\
			                                          </li>\
					                            {{/each}}\
					                            </ul>\
		                        			</div>\
		                        		</div>\
		                        	</div>\
	                        	</div>\
		                        {{/if}}\
		                   	</div>\
		               {{/each}}\
	               	</div>\
		           	<div style='float:right'><a href='#' id='showAll' class='thediv' style='font-weight:bold;position:absolute;right: 38px;bottom: 7px;'>显示全部</a></div>\
	         	</div>\
	        </div>\
        ",
        
        render: function(d)
        {
            if(typeof target == 'object')
            {

                var tpl = this._template
				.replace(/value.name/g, "value." + this["nameField"])
				.replace(/t.name/g, "t." + this["nameField"])
				.replace(/s.name/g, "s." + this["nameField"])
				.replace(/value.id/g, "value." + this["idField"])
				.replace(/t.id/g, "t." + this["idField"])
				.replace(/s.id/g, "s." + this["idField"])
				.replace(/children/g, this["childrenField"])
				.replace(/titleName：/g, this["titleName"]);

                var t = $(target),
					temp = template.compile(tpl),
					html = temp(this.data);
                t.html(html);
                
                if(!this.showAll){
                	$("#showAll").hide();
                	$("#divs_control").find(".title").hide();
                }
                
                this._event();

                //add by fox 2015-03-25
                t.bind("divs_click", function(evt, ids)
                {
                    jQuery(this).find("a.active").removeClass("active");
                    for(var i = 0, len = ids.length; i < len; i++)
                    {
                        jQuery(this).find("a[data-id=" + ids[i] + "]").addClass("active");
                        if(i == len - 1)
                        {
                            $("#divs_control .area-mid .title .thediv").text(jQuery(this).find("a[data-id=" + ids[i] + "]").html());
                            divs.onClick(this, "div", ids);
                        }
                    }
                });
            } else
            {
                return;
            }
            
        },
        _ajax: function(type, url, data)
        {
            return $.ajax({
                data: data,
                url: url,
                contentType: "application/json",
                type: type,
                dataType: "json"
            })
        },
        _event: function()
        {
            $("#showAll").unbind().on("click", function(e)
            {
                $("#divs_control .area-content").find('a').removeClass("active");
                $("#divs_control .area-mid .title .thediv").text(e.target.innerHTML);
                divs.onClick(this, "all");
            })
            $("#divs_control .area-content").find('a').not("#showAll").each(function(index, ele)
            {
                $(ele).click(
                    function(e)
                    {
                        var ids = [];

                        $("#divs_control .area-content").find('a').removeClass("active");
                        $(ele).addClass("active");
                        ids.push("" + $(ele).data("id"));
                        if($(ele).parents(".four-float-right").length > 0)
                        {
                            $(ele).parents(".four-float-right").prev("a").addClass("active");
                            var arr = $(ele).parents(".four-float-right").prev("a");
                            for(var i=0;i<arr.length;i++){
                            	ids.push("" + $(ele).parents(".four-float-right:eq("+i+")").prev("a").data("id"));
                            }
                        }
                        if($(ele).parents(".float-right").length > 0)
                        {
                            $(ele).parents(".float-right").prev("a").addClass("active");
                            ids.push("" + $(ele).parents(".float-right").prev("a").data("id"));
                        }
                        if($(ele).parents(".sub").length > 0)
                        {
                            $(ele).parents(".sub").prev("a").addClass("active");
                            ids.push("" + $(ele).parents(".sub").prev("a").data("id"));
                        }
                        $("#divs_control .area-mid .title .thediv").text(e.target.innerHTML);

                        divs.onClick(ele, "div", ids.reverse());
                    }
                )
            });
            $("#divs_control .area-content").find(".area-root").each(function(index, ele)
            {
                if($(ele).find("li").length > 0)
                {
                    $(ele).hover(function()
                    {
                        $(this).find(".sub").show();
                    }, function()
                    {
                        $(this).find(".sub").hide();
                    })
                }
            })
            
            $(".sub-con .sub-con-data .sub-con-data-detail").find(".three").each(function (index, ele) {
                if ($(ele).find("li").length > 0) {
                    $(ele).hover(function () {
                        $(this).find(".three-div").show();
                        var ch = document.body.clientHeight;
                        var th = $(this).offset().top;
                        var bh = $(this).parents(".sub").prev("a").offset().top;
                        var rh = ch - th - (ch-bh) ;
                        var h=$(this).find(".three-menu-box-detail").height();
                        var w=$(this).find(".three-menu-box-detail").width();
                        var wh=$(this).parents(".sub-con-data-detail").height();
                        window.lw = $(this).offset().left;
                        window.aw = document.body.clientWidth;
                        if(h < rh){
                        	$(this).find(".three-box").css("top",wh-rh+29);
                        	$(this).find(".three-box").css("bottom","");
                        	$(this).find(".three-div").css("top","-28px");
                        	$(this).find(".three-div").css("bottom","");
                        }
                        else{
                        	$(this).find(".three-box").css("bottom","28px");
                        	$(this).find(".three-box").css("top","");
                        	$(this).find(".three-div").css("bottom","-28px");
                        	$(this).find(".three-div").css("top","");
                        }
                        if(lw > (2*aw)/3){
                        	$(this).find(".float-right").css("float","left");
                            $(this).find(".three-div").css("left",-w-5);
                        }
                    }, function () {
                        $(this).find(".three-div").hide();
                    })
                }
            })
            $("#divs_control .area-content").find(".four").each(function(index, ele)
            {
            	if ($(ele).find("li").length > 0) {
                    $(ele).hover(function () {
                    	var id = $(ele).children("a").data("id");
                        $(this).find("div[name="+id+"]").show();
                        var ch = document.body.clientHeight;
                        var th = $(this).offset().top;
                        var rh = ch - th - 34 ;
                        var h=$(this).find("div[name="+id+"]").find(".four-menu-box-detail").height();
                        var w=$(this).find("div[name="+id+"]").find(".four-menu-box-detail").width();
                        if(h < rh){
                        	$(this).find("div[name="+id+"]").css("top","-28px");
                        }
                        else{
                        	$(this).find("div[name="+id+"]").css("bottom",-(rh-28));
                        }
                        if(window.lw > (2*window.aw)/3){
                        	 $(this).find(".four-float-right").css("float","left");
                             $(this).find("div[name="+id+"]").css("left",-w-5);
                        }
                    }, function () {
                    	var id = $(ele).children("a").data("id");
                        $(this).find("div[name="+id+"]").hide();
                    })
                }
            })
            $("#divs_control .area-mid .title").css("cursor", "pointer").click(
               function()
               {
                   $("#divs_control .area-content").toggle();
                   $("#divs_control .gis-icon.icon-arrow-left").toggle();
                   $("#divs_control .gis-icon.icon-arrow-right").toggle();
                   $("#showAll").toggle();
                   if($("#divs_control").css('width') == document.documentElement.clientWidth + 'px')
                   {
                       $("#divs_control").css('width', 'inherit');
                   } else
                   {
                       $("#divs_control").css('width', '100%');
                   }
               }
            )


            this._scroll();

            $("#divs_control").resize(function()
            {
                divs._scroll();
            });


        },
        _scroll: function()
        {
            var th = $("#divs_control .area-content").width() - 180;
            var sh = null;
            $("#divs_control .area-root").each(function()
            {
                sh += $(this).width();
                if(sh > th)
                {
                    $(this).hide();
                } else
                {
                    $(this).show();
                }
            });

            this._redraw();
        },
        _redraw: function()
        {

            var next = $("#divs_control .area-root:visible:last").next();
            if(next.length <= 0)
            {
                $("#divs_control .next").removeClass("btn_active_right").unbind();
            } else
            {
                $("#divs_control .next").addClass("btn_active_right");
            }
            var prev = $("#divs_control .area-root:visible:first").prev();
            if(prev.length <= 0)
            {
                $("#divs_control .prev").removeClass("btn_active_left").unbind();
            } else
            {
                $("#divs_control .prev").addClass("btn_active_left");
            }
            this.prev_next();

        },
        prev_next: function()
        {
            var prev = $("#divs_control .prev");
            var next = $("#divs_control .next");
            if(next.hasClass("btn_active_right"))
            {
                next.unbind().on("click", function()
                {
                    var next_show = $("#divs_control .area-root:visible:last").next(":first");
                    var first_hide = $("#divs_control .area-root:visible:first");
                    first_hide.hide();
                    next_show.show();
                    divs._redraw();
                });
            }
            if(prev.hasClass("btn_active_left"))
            {
                prev.unbind().on("click", function()
                {
                    var prev_show = $("#divs_control .area-root:visible:first").prev(":last");
                    var list_hide = $("#divs_control .area-root:visible:last");
                    list_hide.hide();
                    prev_show.show();
                    divs._redraw();

                })
            }

        }

    }

    $.extend(divs, defaults, options);

    return this.each(function()
    {
        divs.render();
    })


}



//!function (e) { "use strict"; var n = function (e, r) { return n["string" == typeof r ? "compile" : "render"].apply(n, arguments) }; n.version = "2.0.4", n.openTag = "<%", n.closeTag = "%>", n.isEscape = !0, n.isCompress = !1, n.parser = null, n.render = function (e, r) { var t = n.get(e) || a({ id: e, name: "Render Error", message: "No Template" }); return t(r) }, n.compile = function (e, t) { function o(r) { try { return new l(r, e) + "" } catch (i) { return s ? a(i)() : n.compile(e, t, !0)(r) } } var c = arguments, s = c[2], u = "anonymous"; "string" != typeof t && (s = c[1], t = c[0], e = u); try { var l = i(e, t, s) } catch (p) { return p.id = e || t, p.name = "Syntax Error", a(p) } return o.prototype = l.prototype, o.toString = function () { return l.toString() }, e !== u && (r[e] = o), o }; var r = n.cache = {}, t = n.helpers = function () { var e = function (n, r) { return "string" != typeof n && (r = typeof n, "number" === r ? n += "" : n = "function" === r ? e(n.call(n)) : ""), n }, r = { "<": "&#60;", ">": "&#62;", '"': "&#34;", "'": "&#39;", "&": "&#38;" }, t = function (n) { return e(n).replace(/&(?![\w#]+;)|[<>"']/g, function (e) { return r[e] }) }, a = Array.isArray || function (e) { return "[object Array]" === {}.toString.call(e) }, i = function (e, n) { if (a(e)) for (var r = 0, t = e.length; t > r; r++) n.call(e, e[r], r, e); else for (r in e) n.call(e, e[r], r) }; return { $include: n.render, $string: e, $escape: t, $each: i } }(); n.helper = function (e, n) { t[e] = n }, n.onerror = function (n) { var r = "Template Error\n\n"; for (var t in n) r += "<" + t + ">\n" + n[t] + "\n\n"; e.console && console.error(r) }, n.get = function (t) { var a; if (r.hasOwnProperty(t)) a = r[t]; else if ("document" in e) { var i = document.getElementById(t); if (i) { var o = i.value || i.innerHTML; a = n.compile(t, o.replace(/^\s*|\s*$/g, "")) } } return a }; var a = function (e) { return n.onerror(e), function () { return "{Template Error}" } }, i = function () { var e = t.$each, r = "break,case,catch,continue,debugger,default,delete,do,else,false,finally,for,function,if,in,instanceof,new,null,return,switch,this,throw,true,try,typeof,var,void,while,with,abstract,boolean,byte,char,class,const,double,enum,export,extends,final,float,goto,implements,import,int,interface,long,native,package,private,protected,public,short,static,super,synchronized,throws,transient,volatile,arguments,let,yield,undefined", a = /\/\*[\w\W]*?\*\/|\/\/[^\n]*\n|\/\/[^\n]*$|"(?:[^"\\]|\\[\w\W])*"|'(?:[^'\\]|\\[\w\W])*'|[\s\t\n]*\.[\s\t\n]*[$\w\.]+/g, i = /[^\w$]+/g, o = new RegExp(["\\b" + r.replace(/,/g, "\\b|\\b") + "\\b"].join("|"), "g"), c = /^\d[^,]*|,\d[^,]*/g, s = /^,+|,+$/g, u = function (e) { return e.replace(a, "").replace(i, ",").replace(o, "").replace(c, "").replace(s, "").split(/^$|,+/) }; return function (r, a, i) { function o(e) { return m += e.split(/\n/).length - 1, n.isCompress && (e = e.replace(/[\n\r\t\s]+/g, " ").replace(/<!--.*?-->/g, "")), e && (e = x[1] + p(e) + x[2] + "\n"), e } function c(e) { var r = m; if ($ ? e = $(e) : i && (e = e.replace(/\n/g, function () { return m++, "$line=" + m + ";" })), 0 === e.indexOf("=")) { var a = !/^=[=#]/.test(e); if (e = e.replace(/^=[=#]?|[\s;]*$/g, ""), a && n.isEscape) { var o = e.replace(/\s*\([^\)]+\)/, ""); t.hasOwnProperty(o) || /^(include|print)$/.test(o) || (e = "$escape(" + e + ")") } else e = "$string(" + e + ")"; e = x[1] + e + x[2] } return i && (e = "$line=" + r + ";" + e), s(e), e + "\n" } function s(n) { n = u(n), e(n, function (e) { e && !v.hasOwnProperty(e) && (l(e), v[e] = !0) }) } function l(e) { var n; "print" === e ? n = k : "include" === e ? (y.$include = t.$include, n = E) : (n = "$data." + e, t.hasOwnProperty(e) && (y[e] = t[e], n = 0 === e.indexOf("$") ? "$helpers." + e : n + "===undefined?$helpers." + e + ":" + n)), w += e + "=" + n + "," } function p(e) { return "'" + e.replace(/('|\\)/g, "\\$1").replace(/\r/g, "\\r").replace(/\n/g, "\\n") + "'" } var f = n.openTag, d = n.closeTag, $ = n.parser, g = a, h = "", m = 1, v = { $data: 1, $id: 1, $helpers: 1, $out: 1, $line: 1 }, y = {}, w = "var $helpers=this," + (i ? "$line=0," : ""), b = "".trim, x = b ? ["$out='';", "$out+=", ";", "$out"] : ["$out=[];", "$out.push(", ");", "$out.join('')"], T = b ? "$out+=$text;return $text;" : "$out.push($text);", k = "function($text){" + T + "}", E = "function(id,data){data=data||$data;var $text=$helpers.$include(id,data,$id);" + T + "}"; e(g.split(f), function (e) { e = e.split(d); var n = e[0], r = e[1]; 1 === e.length ? h += o(n) : (h += c(n), r && (h += o(r))) }), g = h, i && (g = "try{" + g + "}catch(e){" + "throw {" + "id:$id," + "name:'Render Error'," + "message:e.message," + "line:$line," + "source:" + p(a) + ".split(/\\n/)[$line-1].replace(/^[\\s\\t]+/,'')" + "};" + "}"), g = w + x[0] + g + "return new String(" + x[3] + ");"; try { var j = new Function("$data", "$id", g); return j.prototype = y, j } catch (O) { throw O.temp = "function anonymous($data,$id) {" + g + "}", O } } }(); "function" == typeof define ? define(function () { return n }) : "undefined" != typeof exports && (module.exports = n), e.template = n }(this), function (e) { e.openTag = "{{", e.closeTag = "}}", e.parser = function (n) { n = n.replace(/^\s/, ""); var r = n.split(" "), t = r.shift(), a = r.join(" "); switch (t) { case "if": n = "if(" + a + "){"; break; case "else": r = "if" === r.shift() ? " if(" + r.join(" ") + ")" : "", n = "}else" + r + "{"; break; case "/if": n = "}"; break; case "each": var i = r[0] || "$data", o = r[1] || "as", c = r[2] || "$value", s = r[3] || "$index", u = c + "," + s; "as" !== o && (i = "[]"), n = "$each(" + i + ",function(" + u + "){"; break; case "/each": n = "});"; break; case "echo": n = "print(" + a + ");"; break; case "include": n = "include(" + r.join(",") + ");"; break; default: e.helpers.hasOwnProperty(t) ? n = "=#" + t + "(" + r.join(",") + ");" : (n = n.replace(/[\s;]*$/, ""), n = "=" + n) } return n } }(this.template);
//
//
//$.fn.Divs = function(options)
//{
//    var target = this;
//
//    var defaults = {
//        data: { text: "所有站点", id: "0", children: [{ text: "111111", id: "1", children: [{ text: "432111", id: "3", children: []}] }, { text: "222222", id: "1", children: [] }, { text: "33333", id: "1", children: [] }, { text: "444444", id: "1", children: [] }, { text: "555555", id: "1", children: []}] },
//        nameField: "text",
//        idField: "id",
//        childrenField: "children",
//        showAll:true,
//        titleName:"当前片区",
//        onClick: function(ele, type, ids)
//        {
//
//        }
//    }
//
//    var divs = {
//        _template: "\
//              <div class='area' id='divs_control'>\
//         <div class='area-left'></div>\
//         <div class='area-right'></div>\
//         <div class='area-mid'>\
//           <div class='title'>titleName：<span class='thediv' style='color:#f50'>显示全部</span></div>\
//           <a class='gis-icon icon-arrow-left prev' href='javascript:;'></a>\
//           <a class='gis-icon icon-arrow-right next' href='javascript:;'></a>\
//           <div class='area-content'>\
//               {{each children as value index}}\
//                   <div class='area-root'><a href='#' data-id='{{value.id}}' class='hasConfig' >{{value.name}}</a>\
//                        {{if value.children.length>0}}\
//                        <div class='sub' style='display:none'>\
//                            <ul>\
//                            {{each value.children as t index}}\
//                                <li><a data-id='{{t.id}}'  class='hasConfig'>{{t.name}}</a></li>\
//                            {{/each}}\
//                            </ul>\
//                        </div>\
//                        {{/if}}\
//                   </div>\
//               {{/each}}\
//               </div>\
//                  <div style='float:right'><a href='#' id='showAll' style='color:#f50;position:absolute;right: 38px;bottom: 14px;'>显示全部</a>\
//           </div>\
//         </div>\
//        </div>\
//        ",
//        render: function(d)
//        {
//            if(typeof target == 'object')
//            {
//
//                var tpl = this._template
//				.replace(/value.name/g, "value." + this["nameField"])
//				.replace(/t.name/g, "t." + this["nameField"])
//				.replace(/value.id/g, "value." + this["idField"])
//				.replace(/t.id/g, "t." + this["idField"])
//				.replace(/children/g, this["childrenField"])
//				.replace(/titleName/g, this["titleName"]);
//
//                var t = $(target),
//					temp = template.compile(tpl),
//					html = temp(this.data);
//                t.html(html);
//                
//                if(!this.showAll){
//                	$("#showAll").hide();
//                	$("#divs_control").find(".title").hide();
//                }
//                
//                this._event();
//
//                //add by fox 2015-03-25
//                t.bind("divs_click", function(evt, ids)
//                {
//                    jQuery(this).find("a.active").removeClass("active");
//                    for(var i = 0, len = ids.length; i < len; i++)
//                    {
//                        jQuery(this).find("a[data-id=" + ids[i] + "]").addClass("active");
//                        if(i == len - 1)
//                        {
//                            $("#divs_control .area-mid .title .thediv").text(jQuery(this).find("a[data-id=" + ids[i] + "]").html());
//                            divs.onClick(this, "div", ids);
//                        }
//                    }
//                });
//            } else
//            {
//                return;
//            }
//        },
//        _ajax: function(type, url, data)
//        {
//            return $.ajax({
//                data: data,
//                url: url,
//                contentType: "application/json",
//                type: type,
//                dataType: "json"
//            })
//        },
//        _event: function()
//        {
//            $("#showAll").unbind().on("click", function(e)
//            {
//                $("#divs_control .area-content").find('a').removeClass("active");
//                $("#divs_control .area-mid .title .thediv").text(e.target.innerHTML);
//                divs.onClick(this, "all");
//            })
//            $("#divs_control .area-content").find('a').not("#showAll").each(function(index, ele)
//            {
//                $(ele).click(
//                    function(e)
//                    {
//                        var ids = [];
//
//                        $("#divs_control .area-content").find('a').removeClass("active");
//                        $(ele).addClass("active");
//                        ids.push("" + $(ele).data("id"));
//                        if($(ele).parents(".sub").length > 0)
//                        {
//                            $(ele).parents(".sub").prev("a").addClass("active");
//                            ids.push("" + $(ele).parents(".sub").prev("a").data("id"));
//                        }
//                        $("#divs_control .area-mid .title .thediv").text(e.target.innerHTML);
//
//                        divs.onClick(ele, "div", ids.reverse());
//                    }
//                )
//            });
//            $("#divs_control .area-content").find(".area-root").each(function(index, ele)
//            {
//                if($(ele).find("li").length > 0)
//                {
//                    $(ele).hover(function()
//                    {
//                        $(this).find(".sub").show();
//                    }, function()
//                    {
//                        $(this).find(".sub").hide();
//                    })
//                }
//            })
//            $("#divs_control .area-mid .title").css("cursor", "pointer").click(
//               function()
//               {
//                   $("#divs_control .area-content").toggle();
//                   $("#divs_control .gis-icon.icon-arrow-left").toggle();
//                   $("#divs_control .gis-icon.icon-arrow-right").toggle();
//                   $("#showAll").toggle();
//                   if($("#divs_control").css('width') == document.documentElement.clientWidth + 'px')
//                   {
//                       $("#divs_control").css('width', 'inherit');
//                   } else
//                   {
//                       $("#divs_control").css('width', '100%');
//                   }
//               }
//            )
//
//
//            this._scroll();
//
//            $(window).resize(function()
//            {
//                divs._scroll();
//            });
//
//
//        },
//        _scroll: function()
//        {
//            var th = $("#divs_control .area-content").width() - 100;
//            var sh = null;
//            $("#divs_control .area-root").each(function()
//            {
//                sh += $(this).width();
//                if(sh > th)
//                {
//                    $(this).hide();
//                } else
//                {
//                    $(this).show();
//                }
//            });
//
//            this._redraw();
//        },
//        _redraw: function()
//        {
//
//            var next = $("#divs_control .area-root:visible:last").next();
//            if(next.length <= 0)
//            {
//                $("#divs_control .next").removeClass("btn_active_right").unbind();
//            } else
//            {
//                $("#divs_control .next").addClass("btn_active_right");
//            }
//            var prev = $("#divs_control .area-root:visible:first").prev();
//            if(prev.length <= 0)
//            {
//                $("#divs_control .prev").removeClass("btn_active_left").unbind();
//            } else
//            {
//                $("#divs_control .prev").addClass("btn_active_left");
//            }
//            this.prev_next();
//
//        },
//        prev_next: function()
//        {
//            var prev = $("#divs_control .prev");
//            var next = $("#divs_control .next");
//            if(next.hasClass("btn_active_right"))
//            {
//                next.unbind().on("click", function()
//                {
//                    var next_show = $("#divs_control .area-root:visible:last").next(":first");
//                    var first_hide = $("#divs_control .area-root:visible:first");
//                    first_hide.hide();
//                    next_show.show();
//                    divs._redraw();
//                });
//            }
//            if(prev.hasClass("btn_active_left"))
//            {
//                prev.unbind().on("click", function()
//                {
//                    var prev_show = $("#divs_control .area-root:visible:first").prev(":last");
//                    var list_hide = $("#divs_control .area-root:visible:last");
//                    list_hide.hide();
//                    prev_show.show();
//                    divs._redraw();
//
//                })
//            }
//
//        }
//
//    }
//
//    $.extend(divs, defaults, options);
//
//    return this.each(function()
//    {
//        divs.render();
//    })
//
//
//}