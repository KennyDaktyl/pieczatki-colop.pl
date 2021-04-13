from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic.detail import DetailView
from products.models import Category, Brand, Products
from orders.models import ProductCopy, PayMethod
from orders.constants import DELIVERY_TYPE
from .cart import Cart

import json

# Create your views here.


class AddProduct(View):
    def post(self, request):
        print(request)
        if request.is_ajax():
            color_s = request.POST.get("color_s")
            prod_id = request.POST.get("prod_id")
            prod_org = Products.objects.get(pk=int(prod_id))
            qty = request.POST.get("qty")
            # prod_org.qty -= int(qty)
            # prod_org.save()
            product = ProductCopy()
            product.product_id = prod_org
            product.color_text = color_s
            product.qty = int(qty)
            product.price = prod_org.price
            if prod_org.price_promo:
                product.price = prod_org.price_promo
            product.save()
            cart = Cart(request)
            cart.add(product=product,
                     price=product.price,
                     discount=product.discount,
                     info=product.info,
                     quantity=product.qty)
            dict_obj = {
                'total': float(cart.get_total_price()),
                'len': cart.len(),
                'in_stock': prod_org.qty - int(qty)
            }
            serialized = json.dumps(dict_obj)
            return HttpResponse(serialized)


class EditQtyProduct(View):
    def post(self, request):
        if request.is_ajax():
            prod_id = request.POST.get("prod_id")
            product = ProductCopy.objects.get(pk=int(prod_id))
            qty = int(request.POST.get("qty"))

            cart = Cart(request)
            cart.add(product=product,
                     price=product.price,
                     discount=product.discount,
                     info=product.info,
                     quantity=qty)
            dict_obj = {
                'total': float(cart.get_total_price()),
                'len': cart.len(),
                'in_stock': product.product_id.qty - int(qty)
            }
            serialized = json.dumps(dict_obj)
            return HttpResponse(serialized)


class RemoveProduct(View):
    def post(self, request):
        if request.is_ajax():
            prod_id = request.POST.get("prod_id")
            product = ProductCopy.objects.get(pk=int(prod_id))
            cart = Cart(request)
            cart.remove(product)

            dict_obj = {
                'total': float(cart.get_total_price()),
                'len': cart.len(),
                'in_stock': product.product_id.qty + product.qty
            }
            serialized = json.dumps(dict_obj)
            return HttpResponse(serialized)


class CartDetails(View):
    def get(self, request):
        pay_methods = PayMethod.objects.filter(is_active=True)
        delivery_type = DELIVERY_TYPE
        cart = Cart(request)
        categorys = Category.objects.filter(is_active=True)
        ctx = {
            'cart_ctx': cart,
            'categorys': categorys,
            'pay_methods': pay_methods,
            'delivery_type': delivery_type
        }
        return render(request, "cart/cart_detail.html", ctx)