function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();  //错误信息隐藏
    });
    $("#password").focus(function(){
        $("#password-err").hide();  //错误信息隐藏
    });
    $(".form-login").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        // 将表单的数据存放到对象data中
        var data = {
            mobile: mobile,
            password: passwd
        };
        // 将data转为json字符串
        var jsonData = JSON.stringify(data);
        $.ajax({
            url:"/api/v1.0/session",
            type:"post",
            data: jsonData,
            contentType: "application/json",
            dataType: "json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            success: function (data) {
                if (data.errno == "0") {
                    // 登录成功，跳转到主页
                    location.href = "/index.html";
                }
                else {
                    // 其他错误信息，在页面中展示
                    $("#password-err span").html(data.errmsg);
                    $("#password-err").show();
                }
            }
        });
    });
})