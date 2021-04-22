from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from products.models import Category, Store
from .models import PayMethod, DeliveryMethod, Orders
from .functions import new_number
from .forms import OrderBigForm
from .constants import DELIVERY_TYPE
from cart.cart import Cart
from account.models import Profile, Address
from account.serializers import AddressSerializer

import json
from decimal import Decimal

from account.forms import LoginForm

import stripe
from django.conf import settings

from datetime import datetime

stripe.api_key = settings.STRIPE_SECRET_KEY


@method_decorator(login_required, name="dispatch")
class OrderDetails(View):
    def get(self, request):
        delivery_type = DELIVERY_TYPE
        cart = Cart(request)
        categorys = Category.objects.filter(is_active=True)
        profile = Profile.objects.get(user=request.user.id)
        addresses = Address.objects.filter(user_id=profile.user.id)
        address_default = addresses.filter(main=True).first()

        delivery_methods = DeliveryMethod.objects.filter(is_active=True)
        delivery_default = delivery_methods.filter(default=True).first()

        pay_methods = PayMethod.objects.filter(is_active=True)
        payment_default = pay_methods.filter(default=True).first()

        session_dict = (request.session.get(str(request.user.id)))
        try:
            payment_set = PayMethod.objects.get(pk=session_dict['payment_id'])
            payment_default = PayMethod.objects.get(
                pk=int(session_dict['payment_id']))
        except:
            payment_set = payment_default.id

        try:
            delivery_set = DeliveryMethod.objects.get(
                pk=session_dict['delivery_id'])
            delivery_default = DeliveryMethod.objects.get(
                pk=int(session_dict['delivery_id']))
        except:
            delivery_set = delivery_default.id

        if Decimal(cart.get_total_price()) > 50.00:
            delivery_cost = delivery_default.price_promo
        else:
            delivery_cost = delivery_default.price
        order_price = Decimal(cart.get_total_price()) + Decimal(
            payment_default.price) + Decimal(delivery_cost)
        if profile.company:
            account = 'Firmowe'
            bill = 'Faktura'
            name = profile.business_name
            if profile.business_name_l:
                name_long = profile.business_name_l
            else:
                name_long = False
            nip = profile.nip_number
        else:
            account = 'Indywidualne'
            bill = 'Paragon'
            name = profile.user_id.first_name + " " + profile.user_id.last_name
            name_long = False
            nip = False
        phone = profile.phone_number
        if delivery_default.inpost_box:
            inpost_box = 'sdsdssdsd'
        else:
            inpost_box = False
        if address_default.door:
            street = address_default.street + " " + address_default.house + " / " + address_default.door
        else:
            street = address_default.street + " " + address_default.house
        city = address_default.post_code + ", " + address_default.city
        products_total = round(Decimal(cart.get_total_price()), 2)
        delivery_cost = round(Decimal(delivery_cost), 2)
        payment_cost = round(Decimal(payment_default.price), 2)
        order_total_price = round(
            (products_total + delivery_cost + payment_cost), 2)
        form = OrderBigForm(
            initial={
                'account': account,
                'bill': bill,
                'delivery': delivery_default.name,
                'payment': payment_default.name,
                'name': name,
                'name_long': name_long,
                'nip': nip,
                'phone': phone,
                'street': street,
                'city': city,
                'products_total': products_total,
                'payment_cost': payment_cost,
                'delivery_cost': delivery_cost,
                'order_total_price': order_total_price
            })
        ctx = {
            'client': profile,
            'addresses': addresses,
            'address_default': address_default,
            'cart_ctx': cart,
            'categorys': categorys,
            'pay_methods': pay_methods,
            'payment_set': payment_set,
            'delivery_methods': delivery_methods,
            'delivery_set': delivery_set,
            'delivery_default': delivery_default,
            'payment_default': payment_default,
            'order_price': order_price,
            'form': form,
            'delivery_cost': delivery_cost,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        }
        return render(request, "orders/order_detail.html", ctx)

    def post(self, request):
        cart = Cart(request)
        categorys = Category.objects.filter(is_active=True)
        profile = Profile.objects.get(user=request.user.id)
        addresses = Address.objects.filter(user_id=profile.user.id)
        address_default = addresses.filter(main=True).first()
        delivery_type = DeliveryMethod.objects.filter(is_active=True)
        delivery_default = delivery_type.filter(default=True).first()
        pay_methods = PayMethod.objects.filter(is_active=True)
        payment_default = pay_methods.filter(default=True).first()

        if request.is_ajax():
            if 'address_id' in request.POST:
                address_id = request.POST.get('address_id')
                address = Address.objects.get(pk=address_id)
                address.main = True
                address.save()
                address_serial = AddressSerializer(address)
                return JsonResponse(address_serial.data)
            if 'bill_id' in request.POST:
                bill_id = request.POST.get('bill_id')
                if int(bill_id) == 1:
                    bill_text = 'Paragon'
                else:
                    bill_text = 'Faktura'
                return HttpResponse(bill_text)
            if 'delivery_id' in request.POST:
                delivery_method_price = request.POST.get(
                    'delivery_method_price')
                delivery_id = request.POST.get('delivery_id')
                delivery_method = DeliveryMethod.objects.get(
                    pk=int(delivery_id))
                request.session[str(request.user.id)] = {
                    'payment_id': str(payment_default.id),
                    'delivery_id': delivery_id
                }
                order_price = Decimal(cart.get_total_price()) + Decimal(
                    payment_default.price) + Decimal(
                        delivery_method.price_active(cart))
                return JsonResponse({
                    'delivery_method_price':
                    delivery_method.price_active(cart),
                    'delivery_method_name':
                    delivery_method.name,
                    'order_price':
                    order_price
                })
            if 'payment_id' in request.POST:
                payment_id = request.POST.get('payment_id')
                payment_method = PayMethod.objects.get(pk=int(payment_id))
                request.session[str(request.user.id)] = {
                    'payment_id': payment_id,
                    'delivery_id': str(delivery_default.id)
                }
                order_price = Decimal(cart.get_total_price()) + Decimal(
                    payment_method.price) + Decimal(
                        delivery_default.price_active(cart))
                return JsonResponse({
                    'payment_method_price': payment_method.price,
                    'payment_method_name': payment_method.name,
                    'order_price': order_price
                })
            if 'inpost_box_id' in request.POST:
                inpost_box_id = request.POST.get('inpost_box_id')
                request.session['inpost_box_id'] = inpost_box_id
                return JsonResponse({
                    'inpost_box_id': inpost_box_id,
                })

        if 'checkout' in request.POST:
            form = OrderBigForm(request.POST, None)
            # print(form)
            address_id = request.POST.get('order_total_price')
            print(address_id)
            if form.is_valid():
                return JsonResponse({'id': 2})
                # else:
                #     address_id = request.POST.get('delivery_cost')
                #     print(address_id)
                # delivery_price = form.cleaned_data['delivery_cost']
                # delivery = form.cleaned_data['delivery']
                # payment_price = form.cleaned_data['payment_cost']
                # payment = form.cleaned_data['payment']
                # products_total = form.cleaned_data['products_total']
                # order_total_price = form.cleaned_data['order_total_price']
                #     # # print(delivery_name, delivery_price, payment_name, payment_price,
                #     # #       product_total_price, order_total_price)
                #     # order_total_price = order_total_price.replace(",", ".")
                #     # # order_price = int(Decimal(order_total_price) * 100)
                #     # # print(order_price)
                #     store = Store.objects.all().first()
                #     address = Address.objects.all().first()
                #     payment_name = PayMethod.objects.all().first()
                #     day = datetime.now().day
                #     month = datetime.now().month
                #     year = datetime.now().year
                #     order = Orders()
                #     order.number = new_number(store.id, year, month, day)
                #     order.date = datetime.now()
                #     order.store = store
                #     order.client = request.user
                #     order.type_of_order = delivery
                #     order.address = address
                #     order.pay_method = payment
                #     order.total_price = round(Decimal(order_total_price), 2)
                #     order.save()
                # return JsonResponse({'id': 1})
                # return redirect('checkout_details', order=1)
            else:
                messages.error(request, 'Wystąpił błąd')
                ctx = {'form': form}
                return render(request, "orders/order_detail.html", ctx)


# import requests
# import hashlib


@method_decorator(login_required, name="dispatch")
class InpostBoxSearchView(View):
    def get(self, request):
        return render(request, "orders/inpost_box.html")


class CheckOutDetails(View):
    def get(self, request, order):
        # cart = Cart(request)
        # delivery_type = DeliveryMethod.objects.filter(is_active=True)
        # delivery_default = delivery_type.filter(default=True).first()
        # pay_methods = PayMethod.objects.filter(is_active=True)
        # payment_default = pay_methods.filter(default=True).first()
        # order_price = Decimal(cart.get_total_price()) + Decimal(
        #     payment_default.price) + Decimal(delivery_default.price)
        # order_price = "{0:.2f}".format(order_price / 100)
        # print(order_price)
        order = Orders.objects.get(pk=order)
        order_price = int(order.total_price * 100)
        print(order.total_price)
        print(order.number)
        ctx = {'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY, 'order': order}
        return render(request, "orders/checkout.html", ctx)

    def post(self, request, order):
        # cart = Cart(request)
        # delivery_type = DeliveryMethod.objects.filter(is_active=True)
        # delivery_default = delivery_type.filter(default=True).first()
        # pay_methods = PayMethod.objects.filter(is_active=True)
        # payment_default = pay_methods.filter(default=True).first()
        # if Decimal(cart.get_total_price()) > 50.00:
        #     payment_default.price = 0.00
        #     delivery_default.price = 0.00
        # order_price = Decimal(cart.get_total_price()) + Decimal(
        #     payment_default.price) + Decimal(delivery_default.price)
        # order_price = int(order_price * 100)
        # # order_price = "{0:.2f}".format(order_price[:3])
        # print(order_price)
        order = Orders.objects.get(pk=order)
        order_price = int(order.total_price * 100)
        # # order_price = "{0:.2f}".format(order_price[:3])
        checkout_session = stripe.checkout.Session.create(
            customer_email=request.user.email,
            payment_method_types=['card', 'p24'],
            line_items=[{
                'price_data': {
                    'currency': 'pln',
                    'unit_amount': order_price,
                    'product_data': {
                        'name':
                        'Zamówienie nr :' + order.number,
                        'images': [
                            "https://pieczatki-colop.com/media/images/bcg-stamp_LrTJcQE_YRKH6ut.webp"
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