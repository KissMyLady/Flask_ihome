function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(document).ready(function(){
    //向逻辑区获取城区信息
    $.get("/api/v1.0/areas", function (resp) {
        //校验数据
        if (resp.errno == "0"){
            var areas = resp.data;
            // for (i=0; i <areas.length; i++) {   //注意length这里没有括号
                /*<option value="1">东城区</option>*/
                //var area = areas[i]
                //$("#area-id").append('<option value="'+ area.aid +'">'+ area.aname +'</option>');
            //}
            var html = template("newhouse-areas-templates", {"areas": areas});
            $("#area-id").html(html);
        }
        else {
            alert(resp.errmsg);
        }

    }, "json");

    // 逻辑区(后端) 拦截浏览器请求, 更新请求内容与方式
    $("#form-house-info").submit(function (e) {
        e.preventDefault();

        var data = {};
        $("#form-house-info").serializeArray().map(function (x) {data[x.name] = x.value});
        var facility = [];
        $("#checked[name=facility]").each(function(index, x) {facility[index] = $(x).val()});
        data.facility = facility;

        $.ajax({
            url: "/api/v1.0/houses/info",
            type: "post",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno == "4101"){
                    location.href = "/login.html";
                }
                else if (resp.errno == "0"){
                    $("#form-house-info").hide();
                    $("#form-house-image").show();
                    $("#house-id").val(resp.data.house_id);
                }
                else{
                    alert(resp.errmsg);
                }
            }
        })
    });
    //图片提交ajax
    $("#form-house-image").submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url: "/api/v1.0/houses/image",
            type: "post",
            dataType: "json",
            headers: {
                "X-CSRF-Token": getCookie("csrf_token"),
            },
            success:function (resp) {
                if (resp.errno == "4101"){
                    location.href="/login.html";
                }
                else if (resp.errno == "0"){
                    $(".house-image-cons").append('<img src="' + resp.data.image_url  +  '">')
                }
                else {
                    alert(resp.errmsg);
                }
            }
        })
    })



    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
})