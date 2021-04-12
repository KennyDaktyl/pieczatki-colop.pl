from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from products.models import Category, Brand, Products
from orders.models import ProductCopy
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
            prod_org.qty -= int(qty)
            prod_org.save()
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
                'in_stock': prod_org.qty
            }
            serialized = json.dumps(dict_obj)
            return HttpResponse(serialized)
