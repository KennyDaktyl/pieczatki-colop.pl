$(document).ready(function () {
    var url_address = 'https://sandbox.przelewy24.pl/api/v1/transaction/register'
    var submit = $('#submit');
    console.log('hello_start');

    submit.on("click", function () {
        console.log('hello');
        $.ajax({
            url: url_address,
            type: "POST",
            headers: {
                "Authorization": "Basic " + btoa('124159' + ":" + 'c747dd9c14d86579b65cb9b231c90947')
            },
            data: {
                merchantId: 124159,
                posId: 124159,
                sessionId: "test7",
                amount: 10,
                currency: "PLN",
                }
            //     xhr.setRequestHeader('Authorization', 'Basic ' + btoa(unescape(encodeURIComponent('124159' + ':' + 'c747dd9c14d86579b65cb9b231c90947'))))
            // }
        }).done(function (result) {
            var result_js = $.parseJSON(result);
            console.log(result_js);
        }).fail(function (xhr, status, err) {}).always(function (xhr, status) {});
    });
});