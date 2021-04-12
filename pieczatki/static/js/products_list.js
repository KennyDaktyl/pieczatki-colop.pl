$(document).ready(function () {
    // var url_address = window.location.href;
    var url_address = '/koszyk/dodaj_produkt/'
    var add_product = $('button.add_product');
    
    var total_price = $('#total_price');
    // var total_price_modal = $('#total_price_modal'+prod_id);
    var len = $('#len');
    // var len_modal = $('#len_modal'+prod_id);



    add_product.each(function (index) {
        $(this).on("click", function () {
            var prod_id = $(this).val();
            var qty = $('#qty'+prod_id).val();
            console.log(prod_id);
            console.log(qty);
            var color_s = $('#color_s'+prod_id).val();
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
                $('#total_price_modal'+prod_id).text(result_js['total']);
                len.text(result_js['len'] + 'szt.');
                $('#len_modal'+prod_id).text(result_js['len']);
                in_stock = result_js['in_stock'];
                $('#qty'+prod_id).val(1);
                $('#qty'+prod_id).attr({
                    "max": in_stock,
                    "min": 1
                });
                $('#in_stock_info' + prod_id).text(in_stock + 'szt.');
                $('#add_qty'+ prod_id).text(qty+ 'szt.');
                console.log(in_stock, $('#in_stock_info'+prod_id).val(in_stock + 'szt.'));

            }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
        });
    });
});