/**
 * 
 */



window.mh = {
    All: [],
    MenuTree: {
        sn: 0,
        pid: "cid",
        nm: "配置页面",
        "Children":[{
        sn: 1,
        style: null,
        nm: "页面设置",
        Children: [{
            sn: 11,
            nm: "配置页面",
            Children: [
                {
                    Id: "111",
                    val: "/biz/menu.html",
                    nm: "菜单配置",
                    keep:1
                },
                {
                    Id: "1",
                    val: "/prostock/interfaceconfig.html",
                    nm: "页面配置",
                    keep:1
                },
                {
                    Id: "3",
                    val: "/prostock/admin.html",
                    nm: "接口数据获取",
                    keep:1
                }
            ]
        }]
    },
    {
        sn: 2,
        style: null,
        nm: "基本数据",
        Children: [{
            sn: 12,
            nm: "接口原始数据",
            Children: [{
                    Id: "11",
                    val: "/prostock/interfacedata.html?table_nm=stock_basic",
                    nm: "获取股票基本信息",
                    keep:1
                },
                {
                    Id: "12",
                    val: "/prostock/interfacedata.html?table_nm=hs_const",
                    nm: "沪深股通成份股",
                    keep:1
                }
            ]
        }]
    }

]},
    initMenu:function(){
        let all={}
        function getChildren(menus){
            $.each(menus,function(mi,mv){
                if(mv.val){
                    all[mv.Id]=mv  
                    if(mv.keep=="1"){
                        mh.History.Pages.push(mv);
                        mh.History.Current={"Id":mv.Id,"Item":mv}
                    }
                };
                if (mv.Children&&mv.Children.length>0){
                    getChildren(mv.Children);
                }
            })
        }
        getChildren(mh.MenuTree.Children);
        mh.All=all;
    },
    History: {
        Pages: [

        ],
        Current: {}
        // Current:{"Id":"3","Item": { Id: "3", val: "/prostock/admin.html", nm: "接口数据获取" }}
    },
    uuid: function(len, radix) {
        var chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'.split('');
        var uuid = [],
            i;
        radix = radix || chars.length;

        if (len) {
            // Compact form
            for (i = 0; i < len; i++) uuid[i] = chars[0 | Math.random() * radix];
        } else {
            // rfc4122, version 4 form
            var r;

            // rfc4122 requires these characters
            uuid[8] = uuid[13] = uuid[18] = uuid[23] = '-';
            uuid[14] = '4';

            // Fill in random data.  At i==19 set the high bits of clock sequence as
            // per rfc4122, sec. 4.1.5
            for (i = 0; i < 36; i++) {
                if (!uuid[i]) {
                    r = 0 | Math.random() * 16;
                    uuid[i] = chars[(i == 19) ? (r & 0x3) | 0x8 : r];
                }
            }
        }

        return uuid.join('');
    },
    Open: function(Url, Title) {
        
        var mm = /^([^\?]+)\??/.exec(Url);
        if (mm != null && mm.length > 1) {
            if (Url.startsWith("#")) {
                Url = Url.replace("#", "").replace("!", "");
            }
            var InHistory = false;
            for (var i = 0, Arr = mh.History.Pages, len = Arr.length; i < len; i++) {
                if (Arr[i].val.Trim() == Url.Trim()) {
                    InHistory = true;
                    window.App.$store.commit('selectMenu', Arr[i]);
                    break;
                }
            }

            if (InHistory == false) {
                window.App.$store.commit('addMenu', mh.GetMenuByUrl(Url));
            }
        }
    },
    GetMenuByUrl: function(Url) {
        if (Url.startsWith("#")) {
            Url = Url.replace("#", "");
        }
        var Mi = null;
        for (var Key in mh.All) {
            if (mh.All[Key].val == Url) {
                Mi = mh.All[Key];
                break;
            }
        }
        if (!Mi) {
            var tts = /\?_title=([^&]+)|\&_title=([^&]+)/.exec(Url);
            var Title = "临时页面";
            if (tts && tts.length > 2) {
                Title = tts[1] || tts[2] || Title;
                Title = decodeURIComponent(Title);
            }
            Mi = {
                Id: mh.uuid(8, 16),
                val: Url,
                nm: Title
            };
        }
        return Mi;
    },
    Close: function(Id) {

    },

};

window.onhashchange = function() {
    mh.Open(window.location.hash);
};