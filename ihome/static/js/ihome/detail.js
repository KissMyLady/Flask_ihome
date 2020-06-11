function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function() {
    // 获取详情页面要展示的房屋编号
    var queryData = decodeQuery();
    var houseId = queryData["id"];

    // 获取该房屋的详细信息
    $.get("/api/v1.0/houses/" + houseId, function (resp) {
        if (resp.errno == "0") {
            var html_one = template("house-image-tmpl", {
                img_urls: resp.data.house.img_urls,
                price: resp.data.house.price});

            var html_two = template("house-detail-tmpl", {
                house: resp.data.house});

            $(".swiper-container").html(html_one);
            $(".detail-con").html(html_two);

            // resp.user_id为访问页面用户,resp.data.user_id为房东
            if (resp.data.user_id != resp.data.house.user_id) {
                $(".book-house").attr("href", "/booking.html?hid=" + resp.data.house.hid);
                $(".book-house").show();
            }
            var mySwiper = new Swiper('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            });
        }
    })
})