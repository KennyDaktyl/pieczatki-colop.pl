$(document).ready(function () {
    var stripe = Stripe('pk_test_51IhEZaIs63SrMUIihRzRmqHk8NDqV7NPJqH5OAesgwSo0fhqOUOX5WFHpqtKyUIbzLJaSVaL5u0GRZ4MInd3OU9400GIlwpDni');
    var elements = stripe.elements();

    var options = {
        // Custom styling can be passed to options when creating an Element
        style: {
            base: {
                padding: '10px 12px',
                color: '#32325d',
                fontSize: '16px',
                '::placeholder': {
                    color: '#aab7c4'
                },
            },
        },
    };

    // Create an instance of the p24Bank Element
    var p24Bank = elements.create('p24Bank', options);

    // Add an instance of the p24Bank Element into
    // the `p24-bank-element` <div>
    p24Bank.mount('#p24-bank-element');

    var form = document.getElementById('payment-form');
    var accountholderName = document.getElementById('accountholder-name');
    var accountholderEmail = document.getElementById('accountholder-email');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        // Redirects away from the client
        stripe.confirmP24Payment(
            '{{PAYMENT_INTENT_CLIENT_SECRET}}', {
                payment_method: {
                    p24: p24Bank,
                    billing_details: {
                        name: accountholderName.value,
                        email: accountholderEmail.value,
                    },
                },
                payment_method_options: {
                    p24: {
                        // In order to be able to pass the `tos_shown_and_accepted` parameter, you must
                        // ensure that the P24 regulations and information obligation consent
                        // text is clearly visible to the customer. See
                        // stripe.com/docs/payments/p24/accept-a-payment#requirements
                        // for directions.
                        tos_shown_and_accepted: true,
                    }
                },
                return_url: 'https://pieczatki-colop.com/podsumowanie/platnosci/done/',
            }
        );
    });
});