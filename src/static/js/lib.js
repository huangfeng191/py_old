
function Open(Url, Name)
{
    debugger
    if (Name && Url.indexOf("?") < 0) Url += "?";

    try
    {
        // window.top.location.hash = '#!' + Url + (Name ? "&_title=" + encodeURIComponent(Name) : "");
        window.top.location.hash = Url + (Name ? "&_title=" + encodeURIComponent(Name) : "");
    } catch (e)
    {
        window.location.href = Url + (Name ? "&_title=" + encodeURIComponent(Name) : "");
    }
}


//字符串去除两端空白字符
String.prototype.Trim = function ()
{
    return this.replace(/(^\s*)|(\s*$)/g, "");
};
