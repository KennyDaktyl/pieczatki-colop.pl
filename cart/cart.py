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
        if quantity > 0 and quantity <= product.product_id.qty:
            product_id = str(product.id)
            if product not in self.cart:
                self.cart[product_id] = {
                    'quantity': 0,
                    'price': str(product.price),
                    'discount': str(discount),
                    'info': str(product.info),
                }
            if price:
                self.cart[product_id]['price'] = float(price)
            if discount:
                self.cart[product_id]['discount'] = float(discount)
            if update_quantity:
                self.cart[product_id]['quantity'] = int(quantity)
            else:
                self.cart[product_id]['quantity'] += int(quantity)
            if info:
                self.cart[product_id]['info'] = info

            self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        """
        Usuwanie produktu z koszyka
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """
        Obliczanie wartości koszyka wraz z rabatem
        """

        # item['price'] = (((100 - item['discount']) / 100) +
        #                  item['extra_price'])
        _sum = sum((float(item['price']) *
                    (float((100 - float(item['discount'])) / 100)) *
                    int(item['quantity'])) for item in self.cart.values())
        return round(float(_sum), 2)

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
            item['price'] = round(Decimal(float(item['price'])), 2)
            item['price_netto'] = round(
                float(item['price'] / Decimal("1." + "23")), 2)
            item['discount'] = int(item['discount'])
            # item['total_price'] = int(item['quantity']) * (
            #     (item['price'] * (100 - item['discount'] / 100)))
            item['total_price'] = round(
                Decimal(int(item['quantity']) * float((item['price']))), 2)
            print(item['total_price'])
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
