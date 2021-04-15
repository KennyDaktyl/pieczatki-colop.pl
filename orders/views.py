from django.shortcuts import render
from django.views import View
from products.models import Category
from .models import PayMethod, DeliveryMethod
from .constants import DELIVERY_TYPE
from cart.cart import Cart
from account.models import Profile, Address

import json
from decimal import Decimal


class OrderDetails(View):
    def get(self, request):
        delivery_type = DELIVERY_TYPE
        cart = Cart(request)
        categorys = Category.objects.filter(is_active=True)
        profile = Profile.objects.get(user=request.user.id)
        addresses = Address.objects.filter(user_id=profile.user.id)
        delivery_type = DeliveryMethod.objects.filter(is_active=True)
        delivery_default = delivery_type.filter(default=True).first()
        pay_methods = PayMethod.objects.filter(is_active=True)
        payment_default = pay_methods.filter(default=True).first()
        order_price = Decimal(cart.get_total_price()) + Decimal(
            payment_default.price) + Decimal(delivery_default.price)
        ctx = {
            'client': profile,
            'addresses': addresses,
            'cart_ctx': cart,
            'categorys': categorys,
            'pay_methods': pay_methods,
            'delivery_type': delivery_type,
            'delivery_default': delivery_default,
            'payment_default': payment_default,
            'order_price': order_price
        }
        return render(request, "orders/order_detail.html", ctx)