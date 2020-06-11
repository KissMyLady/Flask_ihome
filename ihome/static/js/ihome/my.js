function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// 点击退出按钮时执行的函数
function logout() {
    $.ajax({
        url: "/api/v1.0/session",    //请求接口删除信息, 带上csrf_token
        type: "delete",              //浏览器默认get请求, 这里用ajax设置为delete请求
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        },
        dataType: "json",
        success: function (resp) {
            if ("0" == resp.errno) {
                location.href = "/index.html";
            }
        }
    });
}

$(document).ready(function(){
    $.get("/api/v1.0/user", function(resp){
        // 用未登录
        if (resp.errno=="4101"){
            location.href = "/login.html";
        }
        else if (resp.errno == "0"){
            $("#user-name").html(resp.data.name);
            $("#user-mobile").html(resp.data.mobile);
            if (resp.data.avatar){
                $("#user-avatar").attr("src", resp.data.avatar);
            }
        }
    }, "json");
})