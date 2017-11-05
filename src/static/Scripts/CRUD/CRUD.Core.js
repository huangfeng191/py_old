
; (function(jQuery)
{
    jQuery.extend(
	{
	    CRUD: function(Container, Options, View)
	    {
	        var Cmp = jQuery(Container).data("component");

	        if(!Cmp)
	        {
	            Cmp = {};
	            View = View || window.CrudView;
	            
	            //注入样式
	            var Skin = jQuery.ImplantStyle("CRUD.Core", (Options.Skin || "Default"));
	            Cmp.Path = Skin.Path;
	            Cmp.View = this.CRUD.View.call(Cmp, Options.View || {});
	            Cmp.Behavior = this.CRUD.Behavior.call(Cmp, Options.Behavior || {});
	            Cmp.Service = this.CRUD.Service.call(Cmp, Options.Service || {}, View);
                Cmp.QueryEnabled = Cmp.FirstQuery = (Options.FirstQuery == false? false:true);
	            Cmp.View.Container = jQuery(Container);

	            jQuery(Container).data("component", Cmp);
	            Cmp.Service.GetView("", Cmp.View.Render);
	        }

	        return Cmp;
	    }
	});
})(jQuery);
