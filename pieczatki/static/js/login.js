$(document).ready(function () {
    var label = $('#id_username');
    label.addClass('col-lg-8');

    var password = $('#id_password');
    password.addClass('col-lg-8');

    FB.getLoginStatus(function (response) {
        statusChangeCallback(response);
    });

});