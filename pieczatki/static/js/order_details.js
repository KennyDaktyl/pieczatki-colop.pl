$(document).ready(function () {
    var url_address = window.location.href;
    var i_close = $('#close');
    var i_open = $('#open');

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
                street_form.text(result.street + ", ");
                house_form.text(result.house);
                door_form.text("/ " + result.door);
                city_form.text(result.city + ", ");
                zip_code_form.text(result.zip_code);

                street_form_big.text(result.street + ", ");
                house_form_big.text(result.house);
                door_form_big.text("/ " + result.door);
                city_form_big.text(result.city + ", ");
                zip_code_form_big.text(result.zip_code);
            }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
        });
    });

    var choice_bill = $('button.choice_bill');
    var bill_form = $('#id_bill');

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
                bill_form.val(result);
            }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
        });
    });

    var div_id_inpost_box = $('#div_id_inpost_box');
    var id_inpost_box = $('#id_inpost_box');
    var delivery_methods = $('div.delivery_methods');
    var id_delivery_name_input = $('#id_delivery');
    var id_delivery_price_input = $('#id_delivery_price_input');
    var id_delivery_price_text = $('#id_delivery_price_text');
    var id_order_total_price_text = $('#id_order_total_price_text');
    var id_order_total_price_input = $('#id_order_total_price_input');
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
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
            }).done(function (result) {
                // var result_js = $.parseJSON(result);
                console.log(result);
                if (result.inpost_box_id == false) {
                    div_id_inpost_box.css('display', 'none');
                } else {
                    div_id_inpost_box.css('display', 'block');
                    id_inpost_box.val(result.inpost_box_id);
                }

                id_delivery_name_input.text(delivery_method_name);
                id_delivery_name_input.val(result.delivery_method_name);

                id_delivery_price_text.text(result.delivery_method_price + " PLN");
                id_delivery_price_input.val(result.delivery_method_price);
                
                order_price = parseFloat(result.order_price).toFixed(2);
                order_price = result.order_price.replace(".", ",");
                id_order_total_price_text.text(order_price + " PLN")
                id_order_total_price_input.val(result.order_price);
            }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
        });
    });

    var payments_methods = $('div.payments');
    var id_payment_form_text = $('#id_payment_form_text');
    var id_payment_form_input = $('#id_payment_form_input');
    var id_payment = $('#id_payment');
    payments_methods.each(function (index) {
        $(this).on("click", function () {
            payments_methods.each(function (index) {
                $(this).removeClass('table-success');
            });
            $(this).addClass('table-success');
            $.ajax({
                url: url_address,
                type: "POST",
                data: {
                    payment_id:  $(this).data('payment_id'),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
            }).done(function (result) {
                // var result_js = $.parseJSON(result);
                order_price = parseFloat(result.order_price).toFixed(2);
                order_price = result.order_price.replace(".", ",");
                id_payment.text(result.payment_method_name);
                id_payment.val(result.payment_method_name);
                id_payment_form_input.val(result.payment_method_price);
                var payment_method_price = parseFloat(result.payment_method_price).toFixed(2);
                payment_method_price = payment_method_price.replace(".", ",");
                id_payment_form_text.text(payment_method_price);
                id_order_total_price_text.text(order_price + " PLN")
                id_order_total_price_input.val(result.order_price);
            }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
        });
    });
});