$(document).ready(function () {
    var url_address = window.location.href;
    var i_close = $('#close');
    var i_open = $('#open');

    var easypack_map = $('#easypack-map');

    window.easyPackAsyncInit = function () {
        easyPack.init({});
        var map = easyPack.mapWidget('easypack-map', function (point) {
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

    var address_form = $('div.address');
    var street_form = $('#street_form');
    var house_form = $('#house_form');
    var door_form = $('#door_form');
    var city_form = $('#city_form');
    var zip_code_form = $('#zip_code_form');
    
    address_form.each(function (index) {
        $(this).on("click", function () {
            address_form.each(function (index) {
                $(this).removeClass('default');
            });
            var address_id = $(this).data('address_id');
            
            $.ajax({
                url: url_address,
                type: "POST",
                data: {
                    address_id: address_id,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
            }).done(function (result) {
                // var result_js = $.parseJSON(result);
                console.log(result);
                $('#address_id' + result.id).addClass('default');
                street_form.text(result.street+", ");
                house_form.text(result.house);
                door_form.text("/ "+result.door);
                city_form.text(result.city+", ");
                zip_code_form.text(result.zip_code);
            }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
        });
    });

    var choice_bill = $('button.choice_bill');
    var bill_form = $('#bill_form');

    choice_bill.each(function (index) {
        $(this).on("click", function () {
            choice_bill.each(function (index) {
                $(this).removeClass('btn-success');
                $(this).addClass('btn-outline-secondary');
            });
            $(this).addClass('btn-success');
            $.ajax({
                url: url_address,
                type: "POST",
                data: {
                    bill_id: $(this).data('bill_id'),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
            }).done(function (result) {
                // var result_js = $.parseJSON(result);
                console.log(result);
                bill_form.text(result);
            }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
        });
    });
});