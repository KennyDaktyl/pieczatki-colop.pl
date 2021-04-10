import random
from decimal import Decimal
from datetime import datetime
from django.conf import settings
from orders.models import ProductCopy

# def new_number(store):
#     year = datetime.now().year
#     month = datetime.now().month
#     day = datetime.now().day
#     number_indx = random.randint(1, 100)
#     number = f"00{number_indx}/{day}/{month}/{year}"
#     return number


class Cart(object):
    def __init__(self, request):
        """
        Inicjalizacja koszyka z produktami
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            #zapis pustego koszyka w sesji
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # self.number = new_number(1)

    def add(self,
            product,
            price,
            discount,
            info,
            quantity=1,
            update_quantity=False):
        """
        Dodanie produktu do koszyka lub edycja parametrów
        """
        product = str(product.id)
        if product not in self.cart:
            self.cart[product] = {
                'quantity': 0,
                'price': str(product.price),
                'discount': str(discount),
                'info': str(info),
            }
        if price:
            self.cart[product_id]['price'] = float(price)
        if discount:
            self.cart[product_id]['discount'] = float(discount)
        if update_quantity:
            self.cart[product_id]['quantity'] = int(quantity)
        else:
            self.cart[product]['quantity'] += int(quantity)
        if info:
            self.cart[product]['info'] = info

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        """
        Usuwanie produktu z koszyka
        """
        product = str(product.id)
        if product in self.cart:
            del self.cart[product]
            self.save()

    def get_total_price(self):
        """
        Obliczanie wartości koszyka wraz z rabatem
        """

        # item['price'] = (
        #     ((100 - item['discount']) / 100) + item['extra_price'])
        return sum(
            round(
                Decimal((float(item['price'] * (float(
                    (100 - float(item['discount'])) / 100)))) *
                        int(item['quantity'])), 2)
            for item in self.cart.values())

    def __iter__(self):
        """
        Iterowanie po produktach w koszyku i pobieranie dancyh z bazy
        """
        products_ids = self.cart.keys()
        products = ProductCopy.objects.filter(pk__in=products_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['discount'] = item['discount']
            item['total_price'] = item['quantity'] * (
                (item['price'] * (100 - int(item['discount'] / 100))))
            yield item

    def len(self):
        """
        Obliczanie sumy elementów w koszyku
        """
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        """Usunięcie koszyka z sesji"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
