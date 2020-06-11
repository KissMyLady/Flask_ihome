function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    $("#form-avatar").submit(function (e) {
        e.preventDefault(); //阻止浏览器默认提交post请求
        //jquery.form.min.js 用插件进行异步提交
        $(this).ajaxSubmit({
            url: "/api/v1.0/user/avatar",
            type: "post",
            dataType: "json",
            headers:{
                "X-CSRFToken": getCookie("csrf_token")
            },
            //回调函数
            success: function (resp) {
                if (resp.errno == "0"){
                    var avatarUrl = resp.data.image_file_name;
                    $("#user-avatar").attr("src", avatarUrl);
                }
                else{
                    alert(resp.errmsg);
                }
            }

        })
        // 使用ajax无法控制data, 所以用到了一个插件, 直接对表单进行异步提交
        // $.ajax({
        //     url: "/api/v1.0/user/avatar",
        //     type: "post",
        //     data: req_json,
        //     contentType: "image/jpg",
        //     headers:{
        //         "X-CSRFToken": getCookie("csrf_token")
        //     },
        //     success: function (resp) {
        //         if (resp.errno == "0"){
        //             location.href = "/my.html"
        //         }
        //         else{
        //             alert(resp.errmsg);
        //         }
        //     }
        // })
    });
    $.get("/api/v1.0/user", function (resp) {
        if (resp.errno == "4104"){
            location.href = "/login.html";
        }
        else if (resp.errno == "0"){
            $("#user-name-profile").html(resp.data.name);
            if (resp.data.avatar){
                $("#user-avatar").attr("src", href=resp.data.avatar);
            }
        }
    }, "json");

    //向后端查询用户信息
    $.get("/api/v1.0/user/auth", function (resp) {
        if (resq.errno == "4101"){
            location.href = "/login.html";
        }
        //查到了用户信息
        else if(resp.errno == "0"){
            $("#user-name").val(resp.data.name);
            if (resp.data.avatar){
                $("#user-avatar").attr("src", resp.data.avatar);
            }
        }
    }, "json");

    // 修改用户名
    $("#form-name").submit(function (e) {
        e.preventDefault();  //阻止默认提交请求
        var name = $("#user-name").val();
        if (!name){
            alert("请填写用户名")
            return;
        }

        $.ajax({
            url: "/api/v1.0/user/auth",
            type: "PUT",
            data: JSON.stringify({name: name}),
            contentType: "application/json",
            dataType: "json",
            headers:{
                "X-CSRFToken": getCookie("csrf_token")
            },
            //回调函数
            success: function (data) {
                if (data.errno == "0"){
                    // 修改成功
                    $(".error-msg").hide();
                    showSuccessMsg();
                }
                else if (data.errno == "4001"){
                    $(".error-msg").show();           //用户名已存在
                }
                else if (data.errno = "4101"){
                    location.href="/register.html";   //用户未登录
                }
            }
        })

    })


})