function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){});
        },1000)
    });
}

$(document).ready(function(){
    // 判断用户是否登录
    $.get("/api/v1.0/session", function(resp) {
        if (resp.errno != "0") {
            location.href = "/login.html";
        }
    }, "json");

    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });

    //价格计算模块
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();  //提取日期
        var endDate = $("#end-date").val();      //提取日期

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg("日期有误，请重新选择!");
        }
        //价格计算
        else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });

    var queryData = decodeQuery();
    var houseId = queryData["hid"];

    // 获取房屋的基本信息
    $.get("/api/v1.0/houses/" + houseId, function(resp){
        if (0 == resp.errno) {
            var img_urls = resp.data.house.img_urls[0];
            var title = resp.data.house.title;
            var price = (resp.data.house.price/100.0).toFixed(0);

            $(".house-info>img").attr("src", img_urls);  //html页面写入数据
            $(".house-text>h3").html(title);             //html页面写入数据
            $(".house-text>p>span").html(price);         //html页面写入数据
        }
    });

    // 订单提交
    $(".submit-btn").on("click", function(e) {
        if ($(".order-amount>span").html()) {
            $(this).prop("disabled", true);
            var startDate = $("#start-date").val();  //提取日期
            var endDate = $("#end-date").val();      //提取日期
            var data = {
                "house_id":houseId,
                "start_date":startDate,
                "end_date":endDate
            };

            alert("order ajax请求 data: "+ data)
            $.ajax({
                url:"/api/v1.0/orders",
                type:"POST",
                data: JSON.stringify(data),
                contentType: "application/json",
                dataType: "json",
                headers:{
                    "X-CSRFTOKEN":getCookie("csrf_token"),
                },
                success: function (resp) {
                    if (resp.errno == "4101") {
                        location.href = "/login.html";
                    }
                    else if (resp.errno == "4004") {
                        showErrorMsg("房间已被抢定，请重新选择日期！");
                    }
                    else if (resp.errno == "0") {
                        location.href = "/orders.html";
                    }
                }
            });
        }
    });
})
