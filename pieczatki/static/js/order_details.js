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

    var address_form_big = $('div.address_big');
    var street_form_big = $('#street_form_big');
    var house_form_big = $('#house_form_big');
    var door_form_big = $('#door_form_big');
    var city_form_big = $('#city_form_big');
    var zip_code_form_big = $('#zip_code_form_big');
    
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
                $('#address_id' + result.id).addClass('default');
                street_form.text(result.street+", ");
                house_form.text(result.house);
                door_form.text("/ "+result.door);
                city_form.text(result.city+", ");
                zip_code_form.text(result.zip_code);

                street_form_big.text(result.street+", ");
                house_form_big.text(result.house);
                door_form_big.text("/ "+result.door);
                city_form_big.text(result.city+", ");
                zip_code_form_big.text(result.zip_code);
            }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
        });
    });

    var choice_bill = $('button.choice_bill');
    var bill_form = $('#bill_form');
    var bill_form_big = $('#bill_form_big');

    choice_bill.each(function (index) {
        $(this).on("click", function () {
            choice_bill.each(function (index) {
                $(this).removeClass('btn-success');
                $(this).addClass('btn-outline-secondary');
            });
            $(this).removeClass('btn-outline-secondary');
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
                bill_form_big.text(result);
            }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
        });
    });

    var delivery_methods = $('div.delivery_methods');
    var delivery_form = $('#delivery_form');
    var delivery_cost_form = $('#delivery_cost_form');
    var delivery_form_big = $('#delivery_form_big');
    var delivery_cost_form_big = $('#delivery_cost_form_big');
    var order_price = $('#order_price');
    delivery_methods.each(function (index) {
        $(this).on("click", function () {
            delivery_methods.each(function (index) {
                $(this).removeClass('table-success');
            });
            $(this).addClass('table-success');
            var delivery_id = $(this).data('delivery_id');
            var delivery_method_price = $('#delivery' + delivery_id).data('price');
            var delivery_method_name = $('#delivery' + delivery_id).data('name');
            $.ajax({
                url: url_address,
                type: "POST",
                data: {
                    delivery_id: delivery_id,
                    delivery_method_name:delivery_method_name,
                    delivery_method_price:delivery_method_price,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
            }).done(function (result) {
                // var result_js = $.parseJSON(result);
                delivery_method_price = parseFloat(delivery_method_price).toFixed(2);
                delivery_method_price = delivery_method_price.replace(".", ",");
                delivery_form.text(result.delivery_method_name);
                delivery_form_big.text(result.delivery_method_name);
                delivery_cost_form.text(delivery_method_price + " PLN");
                delivery_cost_form.data('delivery_cost', delivery_method_price);
                delivery_cost_form_big.text(delivery_method_price + " PLN");
                delivery_cost_form_big.data('delivery_cost', delivery_method_price);
                result.order_price = parseFloat(result.order_price).toFixed(2);
                result.order_price = result.order_price.replace(".", ",");
                order_price.text(result.order_price+" PLN")
            }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
        });
    });

    var payments_methods = $('div.payments');
    var payment_cost_form = $('#payment_cost_form');
    var payment_cost_form_big = $('#payment_cost_form_big');
    var payment_name_form = $('#payment_name_form');
    var payment_name_form_big = $('#payment_name_form_big');
    payments_methods.each(function (index) {
        $(this).on("click", function () {
            payments_methods.each(function (index) {
                $(this).removeClass('table-success');
            });
            $(this).addClass('table-success');
            var payment_id = $(this).data('payment_id');
            var payment_method_price = $('#payment' + payment_id).data('price');
            var payment_method_name = $('#payment' + payment_id).data('name');
            $.ajax({
                url: url_address,
                type: "POST",
                data: {
                    payment_id: payment_id,
                    payment_method_name:payment_method_name,
                    payment_method_price: payment_method_price.replace(',','.'),
                    delivery_method_price:delivery_cost_form.data('delivery_cost').replace(',','.'),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
            }).done(function (result) {
                // var result_js = $.parseJSON(result);
                payment_name_form.text(result.payment_method_name);
                payment_name_form_big.text(result.payment_method_name);
                payment_cost_form.text(payment_method_price + " PLN");
                payment_cost_form_big.text(payment_method_price + " PLN");
                payment_method_price = parseFloat(payment_method_price).toFixed(2);
                payment_method_price = payment_method_price.replace(".", ",");
                payment_cost_form.text(payment_method_price + " PLN");
                payment_cost_form_big.text(payment_method_price + " PLN");
                result.order_price = parseFloat(result.order_price).toFixed(2);
                result.order_price = result.order_price.replace(".", ",");
                order_price.text(result.order_price+" PLN")
            }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
        });
    });
});