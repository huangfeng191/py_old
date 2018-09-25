; (function()
{
    var DftOpts =
	{
        Skin: "Default",
        Exts: "bmp|gif|png|jpg|jpeg",
	    Editable: false,
	    IconSize: "small"//small/big
	};

    //注入样式
    jQuery.ImplantStyle("ImageView");

    jQuery.extend(
	{
	    ImageView: function(Options)
	    {
	        var Cmp =
			{
			    Options: jQuery.extend(true, {}, DftOpts, Options),
			    Show: function(Files, File, Callback)
			    {
			        //打开对话框
			        top.ShowDialog({ Title: Options.Title || "图片浏览", Width: 770, Height: 542, Url: "/static/Scripts/ImageView/dlgImageView.html" }, jQuery.extend(true, {}, Cmp.Options, { Files: Files, File: File },{HasContent:this.Options.HasContent}),
					function(Result)
					{
					    if(Result && Options.Editable && (jQuery.isFunction(Callback) || jQuery.isFunction(Options.OnClose)))
					    {
                            if(jQuery.isFunction(Callback))
                            {
                                Callback(Result);
                            }
                            else
                            {
					            Options.OnClose(Result);
                            }
					    }
					});
			    }
			};

	        return Cmp;
	    }
	});
})();