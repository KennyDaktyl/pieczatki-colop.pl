$(document).ready(function () {
    // var url_address = window.location.href;
    var url_address_edit = '/koszyk/zmien_ilosc/'
    var url_address_del = '/koszyk/usun_produkt/'
    var change_qty = $('button.change_qty');
    var del_prod = $('i.del_prod');

    var empty_basket = $('#empty_basket');
    empty_basket.css('display', 'none')
    var normal_basket = $('#normal_basket');

    var total_price = $('#total_price');
    // var total_price_modal = $('#total_price_modal'+prod_id);
    var len = $('#len');
    // var len_modal = $('#len_modal'+prod_id);

    $('form.form').each(function (index) {
        $(this).on('keyup keypress', function (e) {
            var keyCode = e.keyCode || e.which;
            if (keyCode === 13) {
                e.preventDefault();
                return false;
            }
        });
    });

    change_qty.each(function (index) {
        $(this).on("click", function () {
            var prod_id = $(this).val();
            var qty = $('#qty' + prod_id).val();
            $.ajax({
                url: url_address_edit,
                type: "POST",
                data: {
                    prod_id: prod_id,
                    qty: qty,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
            }).done(function (result) {
                var result_js = $.parseJSON(result);
               
                
                var result_t_netto = result_js['t_netto'];
                result_t_netto = result_t_netto.toFixed(2);
                $('#t_netto' + prod_id).text(result_t_netto + ' PLN');

                var result_t_brutto = result_js['t_brutto'];
                result_t_brutto = result_t_brutto.toFixed(2);
                $('#t_brutto' + prod_id).text(result_t_brutto + ' PLN');
                
                console.log(prod_id,result_t_netto, $('#t_netto' + prod_id));
                var result_total = result_js['total'];
                result_total = result_total.toFixed(2);
                
                var result_total_netto = result_js['total_netto'];
                result_total_netto = result_total_netto.toFixed(2);
                
                var result_len = result_js['len'];
                total_price.text(result_total + ' PLN');
                
                $('#total_price_table').text(result_total + ' PLN');
                $('#total_price_netto_table').text(result_total_netto + ' PLN');
                len.text(result_len + 'szt.');
                $('#len_table').text(result_len + 'szt.');
                in_stock = result_js['in_stock'];
                $('#qty' + prod_id).val(qty);
                $('#qty' + prod_id).attr({
                    "max": in_stock,
                    "min": 1
                });
                $('#in_stock_info' + prod_id).text(in_stock + 'szt.');
                $('#add_qty' + prod_id).text(qty + 'szt.');
                 if (result_len == 0) {
                    empty_basket.css('display', 'block');
                    normal_basket.css('display', 'none');
                } else {
                    empty_basket.css('display', 'none');
                    normal_basket.css('display', 'block');
                };
                console.log(in_stock, $('#in_stock_info' + prod_id).val(in_stock + 'szt.'));

            }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
        });
    });

    del_prod.each(function (index) {
        $(this).on("click", function () {
            var prod_id = $(this).data('product_id');;
            $.ajax({
                url: url_address_del,
                type: "POST",
                data: {
                    prod_id: prod_id,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
            }).done(function (result) {
                var result_js = $.parseJSON(result);
                var result_total = result_js['total'];
                result_total = result_total.toFixed(2);
                total_price.text(result_total + ' PLN');
                var result_total_netto = result_js['total_netto'];
                result_total_netto = result_total_netto.toFixed(2);
                $('#total_price_netto_table').text(result_total_netto + ' PLN');
                $('#total_price_table').text(result_total + ' PLN');

                var result_len = result_js['len'];
                len.text(result_len + 'szt.');
                $('#len_table').text(result_js['len']);
                in_stock = result_js['in_stock'];
                $('#in_stock_info' + prod_id).text(in_stock + 'szt.');
                console.log(in_stock, $('#in_stock_info' + prod_id).val(in_stock + 'szt.'));
                $('#tr' + prod_id).hide();
                
                if (result_len == 0) {
                    empty_basket.css('display', 'block');
                    normal_basket.css('display', 'none');
                } else {
                    empty_basket.css('display', 'none');
                    normal_basket.css('display', 'block');
                };

            }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
        });
    });
});