$(function() {
    window.USBObj = null;
    if ($.browser.msie) {
        window.USBObj = $('<object id="ePass" style="display:none; left: 0px; top: 0px" height="0" width="0" classid="clsid:0272DA76-96FB-449E-8298-178876E0EA89" viewastext></object>')
            .appendTo("html");
    }

    $(document).ready(function() {
        //setVisible(["username", "password"]);
    });

    $("#password").on("keypress", function(event) {
        if (event.keyCode == 13) {
            $("#submit").trigger("click");
        }
    });

    $(".captcha").click(function() {
        var src = $(this).attr('src');
        var index = src.indexOf("?");
        if (index != -1) {
            src = src.substring(0, index + 1);
        }

        src += $.now();
        $(this).attr('src', src);
    });

    $(".input").keydown(function() {
        var id = $(this).attr("id");
        if ($(this).val() == "") {
            $("." + id).show();
        } else {
            $("." + id).hide();
        }
    });

    $(".input").keyup(function() {
        var id = $(this).attr("id");
        if ($(this).val() == "") {
            $("." + id).show();
        } else {
            $("." + id).hide();
        }
    });

    $(".input").change(function() {
        $(".error").empty("").hide();
    });

    $("#forreg #reg").click(function() {
        if (!validate1()) return false;

        var obj = $("#regFm").serializeJSON();
            delete obj["pwd1"];
        var url = $('#regFm').attr("action");
        $.ajax({
            type: 'POST',
            dataType: 'json',
            contentType: "application/json; charset=UTF-8",
            url: url,
            data: JSON.stringify({ "record": obj } || {}),
            success: function(data) {
                var code = data.Code;

                if (code == 0) {
                    $(".error").html("注册成功，请登录").show();
                    $("#forreg input[type!='button']").val("");
                    $("#forreg").css("display", "none")

                } else {

                    var id = '#username';
                    var msg = "用户名或密码错误";
                    if (code == 80001) {
                        id = '#username';
                        msg = "请输入用户名";

                    } else {
                        msg = data.Message;
                    }
                    $(id).focus();
                    $(".error1").html(msg).show();
                }
            },
            error: function(e) {
                $(".error1").html("注册失败,请重试").show();
            }
        })
    });

    $("#register").click(function() {
        $("#forreg").css("display", "block")
    });
    $("#forreg #cancel").click(function() {
        $("#forreg input[type!='button']").val("");
        $(".error1").html("");
        $("#forreg").css("display", "none")
    });
    $("#submit").click(function() {
        //$(".error").empty("").hide();

        if (!validate()) return false;

        var obj = $("#loginFm").serializeJSON();
        var url = $('#loginFm').attr("action");
        obj.remember = $("#remember").prop("checked") ? 1 : 0;
        // if (!USBCheck()) {
        //     return;
        // }

        var newWin;
        if ($.browser.msie && GotoType == 1) {
            newWin = window.open("", "", "location=no,menubar=no,resizable=no,scrollbars=no,titlebar=no,toolbar=no," +
                "status=no,z-look=yes,top=0,left=0,width=" + (window.screen.availWidth - 10) +
                ",height=" + (window.screen.availHeight - 26));
            newWin.document.write("请稍候...");
        }

        obj['ishd'] = Proxy.GetUrlParam("forced") == null || Proxy.GetUrlParam("forced") == "0" ? false : true;

        $.ajax({
            type: 'POST',
            dataType: 'json',
            contentType: "application/json; charset=UTF-8",
            url: url,
            data: JSON.stringify(obj || {}),
            success: function(data) {
                var code = data.Code;

                if (code == 0) {
                    if (newWin) {
                        newWin.document.write("登录成功,正为您跳转到主页...");
                        newWin.location.replace(data.Response.redirect);
                        if (/(iPhone|iPad|iPod|iOS)/i.test(navigator.userAgent)) {
                            newWin.location.replace("/jsb/ipadanalysis.html");
                        } else {
                            newWin.location.replace(data.Response.redirect);
                        }
                        window.opener = null;
                        window.open("", "_self");
                        window.close();
                    } else {
                        $(".error").html("登录成功,正为您跳转到主页...").show();

                        if (/(iPhone|iPad|iPod|iOS)/i.test(navigator.userAgent)) {
                            window.location.replace("/jsb/ipadanalysis.html");
                        } else {
                            window.location.replace(data.Response.redirect);
                        }

                    }
                } else {
                    if (newWin) {
                        newWin.close();
                    }
                    var id = '#username';
                    var msg = "用户名或密码错误";
                    if (code == 80001) {
                        id = '#username';
                        msg = "请输入用户名";
                    } else if (code == 80002) {
                        id = '#password';
                        msg = "请输入密码";
                    } else if (code == 80004) {
                        msg = "该账号已锁定";
                    } else if (code == 80006) {
                        msg = "不支持网页登录";
                    } else if (code == 2) {
                        id = '#captcha';
                        msg = "验证码输入有误";
                    } else if (code == 7) {
                        id = '#captcha';
                        msg = "请输入验证码";
                    } else if (code == 80008) {
                        id = '#captcha';
                        msg = "此帐号不允许登录";
                    } else {
                        msg = data.Message;
                    }
                    $(id).focus();
                    $(".error").html(msg).show();
                }
            },
            error: function(e) {
                $(".error").html("登录失败,请重试").show();
            }
        })
    })


    var typeIndex = window.location.href.indexOf('admin');

    var un, pw, isRemember

    if (typeIndex > 0) {
        un = getCookie("aun")
        pw = getCookie("apw")
        isRemember = getCookie("arem")
    } else {
        un = getCookie("un")
        pw = getCookie("pw")
        isRemember = getCookie("rem")
    }

    if (isRemember && isRemember != '0') {

        if (un) $("#username").val(un);
        if (pw) $("#password").val(pw);

        if (isRemember == '1') {
            $("#remember").trigger("click");
            //$("#captcha").focus();
        }
    }
});

function setVisible(ids) {
    for (var i = 0; i < ids.length; i++) {
        var id = ids[i];
        if ($("#" + id).val() == "") {
            $("." + id).show();
        } else {
            $("." + id).hide();
        }
    }
}

function validate() {

    var valid = true;
    var msg = '';
    var id = '#username';

    var username = $.trim($('#username').val());
    var password = $.trim($('#password').val());
    var captcha = 'empty'; //$.trim($('#captcha').val());

    if (username == '') {
        msg = '请输入用户名';
        id = "#username";
        valid = false;
    } else if (password == '') {
        msg = '请输入密码';
        id = "#password";
        valid = false;
    } else if (captcha == '') {
        msg = '请输入验证码';
        id = "#captcha";
        valid = false;
    }

    $(id).focus();
    $(".error").html(msg).show();

    return valid;
}


function validate1() {

    var valid = true;
    var msg = '';
    var id = '#acc';

    var acc = $.trim($('#acc').val());
    var nm = $.trim($('#nm').val());
    var mobi = $.trim($('#mobi').val());
    var pwd = $.trim($('#pwd').val());
    var pwd1 = $.trim($('#pwd1').val());


    if (acc == '') {
        msg = '请输入客户代码';
        id = "#acc";
        valid = false;
    } else if (nm == '') {
        msg = '请输入姓名';
        id = "#nm";
        valid = false;
    } else if (mobi == '') {
        msg = '请输入手机';
        id = "#mobi";
        valid = false;
    } else if (pwd == '') {
        msg = '请输入密码';
        id = "#pwd";
        valid = false;
    } else if (pwd1 == '') {
        msg = '请输入确认密码';
        id = "#pwd1";
        valid = false;
    } else if (pwd != pwd1) {
        msg = '两次密码输入不一致，请重新输入';
        $('#pwd').val("");
        $('#pwd1').val("");
        id = "#pw";
        valid = false;
    }


    $(id).focus();
    $(".error1").html(msg).show();

    return valid;
}


// utility function called by getCookie()
function getCookieVal(offset) {
    var endstr = document.cookie.indexOf(";", offset);
    if (endstr == -1) {
        endstr = document.cookie.length;
    }
    var a = document.cookie.substring(offset, endstr);
    return decodeURIComponent(document.cookie.substring(offset, endstr));
}

// primary function to retrieve cookie by name
function getCookie(name) {
    var arg = name + "=";
    var alen = arg.length;
    var clen = document.cookie.length;
    var i = 0;
    while (i < clen) {
        var j = i + alen;
        if (document.cookie.substring(i, j) == arg) {
            return getCookieVal(j);
        }
        i = document.cookie.indexOf(" ", i) + 1;
        if (i == 0) break;
    }
    return null;
}

function USBCheck() {
    var href = window.location.href;
    var intranet =
        href.indexOf("http://127.") == 0 ||
        href.indexOf("https://127.") == 0 ||
        href.indexOf("http://localhost") == 0 ||
        href.indexOf("https://localhost") == 0 ||
        href.indexOf("http://192.168.") == 0 ||
        href.indexOf("https://192.168.") == 0 ||
        href.indexOf("http://172.") == 0 ||
        href.indexOf("https://172.") == 0;
    //内网环境或不须USBKEY登录
    if (intranet || Smdl != 3) {
        return true;
    }
    if (!$.browser.msie || !window.USBObj) {
        alert("对不起，本系统仅支持IE浏览器！");
        return false;
    }
    var flag = true;
    window.USBObj.each(function() {
        var o = this;
        try {
            o.GetLibVersion();
        } catch (e) {
            flag = false;
            alert("未检测到USB-Key驱动程序，点击进入安装页...");
            window.location.href = "/static/webinst/welcome.html";
            throw "Unknow Error";
        }
        try {
            o.OpenDevice(1, "")
            o.GetStrProperty(0x07, 0, 0);
        } catch (e) {
            flag = false;
            alert("为保证系统安全，请插入USB-Key！");
            throw "Unknow Error";
        } finally {
            o.CloseDevice()
        }
        try {
            o.OpenDevice(1, "")
            o.VerifyPIN(0, "0573-82229995");
        } catch (e) {
            flag = false;
            alert("USB-Key验证失败，请重试或联系系统管理员！");
            throw "Unknow Error";
        } finally {
            o.CloseDevice();
        }
    });
    return flag;
}