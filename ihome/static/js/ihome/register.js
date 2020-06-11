function getCookie(name) { //js读取cookie的方法
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}//"csrf_token=IjExMWZhMjNjMGE5OWI5ZWExZjliMDRlMTA2ZWY5NjJlNWMxZDdiNTAi.Xti3Dw.hElh5734X2EqnffgiKJVOlAzop8"

// 保存图片验证码编号
var imageCodeId = ""; //这里设置成了全局变量, 方便下面60s验证使用

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now();  //use high-precision timer if available
    }
    //防盗
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

function generateImageCode() {
    // 形成图片验证码的后端地址， 设置到页面中，让浏览请求验证码图片
    // 1. 生成图片验证码编号
    imageCodeId = generateUUID();
    // 是指图片url
    var url = "/api/v1.0/image_code/" + imageCodeId;
    $(".image-code img").attr("src", url);
}

function sendSMSCode() {
    $(".phonecode-a").removeAttr("onclick");  //移除可能二次触发的情况
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");  //恢复触发
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }

    //http://127.0.0.1:5000/api/v1.0/sms_code/13207297072?image_code=COMR&image_code_id=11
    //ajax请求
    var req_data = {
        image_code: imageCode,          // 图片验证码的值
        image_code_id: imageCodeId      // 图片验证码的编号，（全局变量）
    };
    //{mobile:mobile, image_code:imageCode, image_code_id:imageCodeId},
    $.get("/api/v1.0/sms_code/"+ mobile, req_data, function(data){ //data是后端相应值
            if (0 != data.errno) {
                $("#image-code-err span").html(data.errmsg); 
                $("#image-code-err").show();
                if (2 == data.errno || 3 == data.errno) {
                    generateImageCode();
                }
                $(".phonecode-a").attr("onclick", "sendSMSCode();");
            }   
            else {
                //发送成功
                var $time = $(".phonecode-a");
                var duration = 60;
                var intervalid = setInterval(function(){
                    $time.html(duration + "秒"); 
                    if(duration === 1){
                        clearInterval(intervalid);
                        $time.html('获取验证码'); 
                        $(".phonecode-a").attr("onclick", "sendSMSCode();");
                    }
                    duration = duration - 1;
                }, 1000, 60); 
            }
    }, 'json'); 
}

$(document).ready(function() {
    generateImageCode();
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });
    $(".form-register").submit(function(e){//提交事件e
        e.preventDefault();//阻止浏览器对于表单的默认自动行为
        var mobile = $("#mobile").val();
        var phoneCode = $("#phonecode").val();
        var passwd = $("#password").val();
        var passwd2 = $("#password2").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!phoneCode) {
            $("#phone-code-err span").html("请填写短信验证码！");
            $("#phone-code-err").show();
            return;
        }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        if (passwd != passwd2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            return;
        }
        //调用ajax向后端发送请求
        var req_data = {
         mobile : mobile,
         sms_code :phoneCode,
         password  :passwd,
         password2 :passwd2
        }
        //转换成json数据
        var req_json = JSON.stringify(req_data)
        $.ajax({
            url : "/api/v1.0/users",
            type: "post",
            data: req_json,
            contentType: "application/json",
            headers: {
              "X-CSRFToken": getCookie("csrf_token")

            },//请求头, 将csrf值放入请求头中, 方便 flaks的csrf验证
            success: function (resp) {
                if (resp.errno == "0"){
                    //注册成功, 跳转主页
                    location.href = "/index.html"
                }
                else {
                    alert(resp.errmsg);
                }
            }
        })
    });
})