from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from products.models import Category
from .models import PayMethod, DeliveryMethod
from .constants import DELIVERY_TYPE
from cart.cart import Cart
from account.models import Profile, Address

import json
from decimal import Decimal

from account.forms import LoginForm

import stripe

stripe.api_key = "sk_test_51IhEZaIs63SrMUIijVMnqrGqnKdsUMAEbrW8S6HcVXKV9kcqQaLHQgBAwcPbi2npi6KPNPuhnHu38AjuaYEMhR1e00hx2DhSpM"


class OrderDetails(View):
    def get(self, request):
        delivery_type = DELIVERY_TYPE
        cart = Cart(request)
        categorys = Category.objects.filter(is_active=True)
        profile = Profile.objects.get(user=request.user.id)
        addresses = Address.objects.filter(user_id=profile.user.id)
        address_default = addresses.filter(main=True).first()
        delivery_type = DeliveryMethod.objects.filter(is_active=True)
        delivery_default = delivery_type.filter(default=True).first()
        pay_methods = PayMethod.objects.filter(is_active=True)
        payment_default = pay_methods.filter(default=True).first()
        order_price = Decimal(cart.get_total_price()) + Decimal(
            payment_default.price) + Decimal(delivery_default.price)

        form = LoginForm()
        ctx = {
            'client': profile,
            'addresses': addresses,
            'address_default': address_default,
            'cart_ctx': cart,
            'categorys': categorys,
            'pay_methods': pay_methods,
            'delivery_type': delivery_type,
            'delivery_default': delivery_default,
            'payment_default': payment_default,
            'order_price': order_price,
            'form': form
        }
        return render(request, "orders/order_detail.html", ctx)


import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

# import requests
# import hashlib


class CheckOutDetails(View):
    def get(self, request):
        cart = Cart(request)
        delivery_type = DeliveryMethod.objects.filter(is_active=True)
        delivery_default = delivery_type.filter(default=True).first()
        pay_methods = PayMethod.objects.filter(is_active=True)
        payment_default = pay_methods.filter(default=True).first()
        order_price = Decimal(cart.get_total_price()) + Decimal(
            payment_default.price) + Decimal(delivery_default.price)
        print(order_price)
        ctx = {'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY}
        return render(request, "orders/checkout.html", ctx)

    def post(self, requset, *args, **kwargs):
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card', 'p24'],
            line_items=[{
                'price_data': {
                    'currency': 'pln',
                    'unit_amount': 700,
                    'product_data': {
                        'name':
                        'Pieczątka Colop Compact 20',
                        'images': [
                            'https://pieczatki-colop.com/media/images/pieczatki-budowlane.webp'
                        ],
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://onet.pl',
            cancel_url='https://wp.pl',
        )
        return JsonResponse({'id': checkout_session.id})

        # session_key = request.COOKIES[settings.SESSION_COOKIE_NAME]
        # r = requests.get(
        #     'https://sandbox.przelewy24.pl/api/v1/payment/methods/pl',
        #     auth=('124159', 'c747dd9c14d86579b65cb9b231c90947'))
        # r = json.loads(r.text)
        # sign = {
        #     "sessionId": session_key,
        #     "merchantId": 124159,
        #     "amount": 100,
        #     "currency": "PLN",
        #     "crc": 'ffdcf444a8150523'
        # }
        # sign = json.dumps(sign)
        # m = hashlib.sha384(sign.encode('utf-8')).hexdigest()
        # print(m)
        # data = {
        #     "merchantId":
        #     124159,
        #     "posId":
        #     124159,
        #     "sessionId":
        #     session_key,
        #     "amount":
        #     100,
        #     "currency":
        #     "PLN",
        #     "description":
        #     "test order",
        #     "email":
        #     "john.doe@example.com",
        #     "client":
        #     "string",
        #     "address":
        #     "string",
        #     "zip":
        #     "string",
        #     "city":
        #     "string",
        #     "country":
        #     "PL",
        #     "phone":
        #     "string",
        #     "language":
        #     "pl",
        #     "method":
        #     0,
        #     "urlReturn":
        #     "https://onet.pl/",
        #     "urlStatus":
        #     "string",
        #     "timeLimit":
        #     0,
        #     "channel":
        #     1,
        #     "waitForResult":
        #     False,
        #     "regulationAccept":
        #     False,
        #     "shipping":
        #     0,
        #     "transferLabel":
        #     "string",
        #     "mobileLib":
        #     1,
        #     "sdkVersion":
        #     "string",
        #     "sign":
        #     "2a5bf288cec31609178b8dfc18ac9617793b70a31c8503491aaf147053bc43b29a72391cf8bc37d50bfc1ef92d27bfcf",
        #     "encoding":
        #     "UTF-8",
        #     "methodRefId":
        #     "string",
        #     "cart": [{
        #         "sellerId": "test50",
        #         "sellerCategory": "test",
        #         "name": "test product",
        #         "description": "test",
        #         "quantity": 1,
        #         "price": 1,
        #         "number": "1"
        #     }],
        #     "additional": {
        #         "shipping": {
        #             "type": 0,
        #             "address": "string",
        #             "zip": "00-000",
        #             "city": "string",
        #             "country": "string"
        #         }
        #     }
        # }
        # auth = ('124159', 'c747dd9c14d86579b65cb9b231c90947')
        # headers = {
        #     'Content-type': 'application/json',
        #     'Accept': 'text/plain',
        # }
        # url = 'https://sandbox.przelewy24.pl/api/v1/transaction/register'
        # r = requests.post(url,
        #                   data=json.dumps(data),
        #                   headers=headers,
        #                   auth=auth)
        # p = requests.get(
        #     'https://sandbox.przelewy24.pl/api/v1/transaction/register',
        #     auth=('124159', 'c747dd9c14d86579b65cb9b231c90947'),
        #     data=data)
        # print(r, p)

        # ctx = {'methods': r}