function hrefBack() {
    history.go(-1);
}

// 解析提取url中的查询字符串参数
function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    // 获取房屋编号
    var queryData = decodeQuery();
    var houseId = queryData["id"];

    // 获取该房屋的详细信息
    $.get("/api/v1.0/houses/"+ houseId, function(resp){
        //校验
        if (resp.errno == "0" || resp.errno == 0) {
            var img_urls = resp.data.house.img_url;
            var price = resp.data.house.price;
            var houses = resp.data.house;
            var html_one_a = template("house-image-tmpl", {"img_urls": img_urls, "price": price});
            var html_two_b = template("house-detail-tmpl", {"house": houses});

            $(".swiper-container").html(html_one_a);
            $(".detail-con").html(html_two_b);

            //resp.user_id为访问页面用户,resp.data.user_id为房东
            if (resp.data.user_id != resp.data.house.user_id) {
                $(".book-house").attr("href", "/booking.html?hid=" + resp.data.house.hid);
                $(".book-house").show();
            }

            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: ".swiper-pagination",
                paginationType: "fraction"
            });
        }
        else {
            alert(resp.errmsg);
        }
    });
})