$(document).ready(function () {
    var url_address = window.location.href;
    var i_close = $('#close');
    var i_open = $('#open');

    var easypack_map = $('#easypack-map');

    window.easyPackAsyncInit = function () {
        easyPack.init({});
        var map = easyPack.mapWidget('easypack-map', function(point){
            console.log(point);
            easypack_map.removeClass('show');
        });
    };
    var open_geo = $('#open_geo');
    open_geo.on("click", function () {
        easypack_map.toggleClass('show');
    });

    var order_details = $('#order_details');

    var menu_burger = $('#menu_burger');
    menu_burger.on("click", function () {
        order_details.css('z-index', '1');
    });

    $('#form').on('keyup keypress', function (e) {
        var keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
            e.preventDefault();
            return false;
        }
    });


    i_close.on("click", function () {
        order_details.toggleClass('slider');
        i_close.css('display', 'none');
        i_open.css('display', 'block');
    });

    i_open.on("click", function () {
        order_details.toggleClass('slider');
        i_close.css('display', 'block');
        i_open.css('display', 'none');
    });

    
});