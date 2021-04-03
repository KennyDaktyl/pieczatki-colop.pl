$(document).ready(function () {
    var top = $('#top');
    var nav = $('#nav');
    var page = $('#page');

    top_height = top.height();
    nav_height = nav.height();
    nav.css('margin-top', top_height);
    page.css('margin-top', top_height + nav_height+20);
    console.log(top_height + nav_height);
    $(window).on('wheel', function (event) {
        if (event.originalEvent.deltaY < 0) {
            top.removeClass('scroll_down');
            nav.removeClass('active');
        } else {
            top.addClass('scroll_down');
            nav.addClass('active');
        }
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


})