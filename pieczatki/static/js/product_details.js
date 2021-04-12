$(document).ready(function () {
    // var url_address = window.location.href;
    var url_address = '/koszyk/dodaj_produkt/'
    var add_product = $('#add_product');
    var prod_id = $('#prod_id').val();
    var total_price = $('#total_price');
    var total_price_modal = $('#total_price_modal');
    var len = $('#len');
    var add_product = $('#add_product');
    var len_modal = $('#len_modal');

    $('#form').on('keyup keypress', function (e) {
        var keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
            e.preventDefault();
            return false;
        }
    });

    add_product.on("click", function () {
        var qty = $('#qty').val();
        var color_s = $('#color_s').val();
        $.ajax({
            url: url_address,
            type: "POST",
            data: {
                prod_id: prod_id,
                qty: qty,
                color_s: color_s,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
        }).done(function (result) {
            var result_js = $.parseJSON(result);
            total_price.text(result_js['total']);
            total_price_modal.text(result_js['total']);
            len.text(result_js['len'] + 'szt.');
            len_modal.text(result_js['len']);
            in_stock = result_js['in_stock'];
            $('#qty').val(0);
            $('#qty').attr({
                "max": in_stock,
                "min": 0
            });
            $('#in_stock_info').text(in_stock + 'szt.');
            $('#add_qty').text(qty + 'szt.');
            console.log(in_stock, $('#in_stock_info').val(in_stock + 'szt.'));

        }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
    });
});