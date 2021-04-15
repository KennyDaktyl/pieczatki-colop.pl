$(document).ready(function () {
    var top = $('#top');
    var nav = $('#nav');
    var page = $('#page');
    var link_map = $('#link_map');
    var navbarTogglerDemo03 = $('#navbarTogglerDemo03');

    top_height = top.height();
    nav_height = nav.height();
    link_map_height = link_map.height();
    // nav.css('margin-top', top_height);
    // navbarTogglerDemo03.css('margin-top', link_map_height);
    // link_map.css('margin-top', top_height + nav_height+ 15);
    // page.css('margin-top', top_height + nav_height + link_map_height + 20);
    // $(window).on('wheel', function (event) {
    //     if (event.originalEvent.deltaY < 0) {
    //         top.removeClass('scroll_down');
    //         nav.removeClass('active');
    //     } else {
    //         top.addClass('scroll_down');
    //         nav.addClass('active');
    //     }
    // });

    var menu_burger = $('#menu_burger');
    var stamp_logo = $('#stamp_logo');
    menu_burger.on("click", function () {
        stamp_logo.toggleClass('show');
    });


    var lastY;
    $(window).bind('touchmove', function (e) {
        var currentY = e.originalEvent.touches[0].clientY;
        if (currentY > lastY) {
            top.removeClass('scroll_down');
            nav.removeClass('active');
        } else if (currentY < lastY) {
            top.addClass('scroll_down');
            nav.addClass('active');
        }
        lastY = currentY;
    });

    function refreshPage() {
        var page_y = $(document).scrollTop();
        window.location.href = window.location.href + '?page_y=' + page_y;
    }
    document.addEventListener("DOMContentLoaded", function (event) {
        var scrollpos = localStorage.getItem('scrollpos');
        if (scrollpos) window.scrollTo(0, scrollpos);
    });

    window.onbeforeunload = function (e) {
        localStorage.setItem('scrollpos', window.scrollY);
    };

    // var dropdown_basket = $('#dropdown_basket');
    // var basket_div = $('#basket_div');
    // dropdown_basket.click(function () {
    //     basket_div.toggleClass('show');

    // });
})