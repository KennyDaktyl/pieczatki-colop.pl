$(document).ready(function () {
    var url_address = window.location.href;
    var i_close = $('#close');
    var i_open = $('#open');
    
    var order_details = $('#order_details');

    $('#form').on('keyup keypress', function (e) {
        var keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
            e.preventDefault();
            return false;
        }
    });

    menu_burger.on("click", function () {
        stamp_logo.toggleClass('show');
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