from django.shortcuts import render
from django.views import View
from products.models import Category
from .models import PayMethod, DeliveryMethod
from .constants import DELIVERY_TYPE
from cart.cart import Cart
from account.models import Address

import json


class OrderDetails(View):
    def get(self, request):
        delivery_type = DELIVERY_TYPE
        cart = Cart(request)
        categorys = Category.objects.filter(is_active=True)
        client = request.user
        addresses = Address.objects.filter(user_id=client)
        delivery_type = DeliveryMethod.objects.filter(is_active=True)
        pay_methods = PayMethod.objects.filter(is_active=True)
        ctx = {
            'client': client,
            'addresses': addresses,
            'cart_ctx': cart,
            'categorys': categorys,
            'pay_methods': pay_methods,
            'delivery_type': delivery_type
        }
        return render(request, "orders/order_detail.html", ctx)