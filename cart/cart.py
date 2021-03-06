import random
from decimal import Decimal
from datetime import datetime
from django.conf import settings
from orders.models import ProductCopy, DeliveryMethod, PayMethod
from orders.serializers import ProductCopySerializer

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
        # self.delivery = {}
        # self.payment = {}
        # self.inpost_box = {}

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
                    # 'color_text': str(get_color_text_display()),
                    'price': str(product.price),
                    'discount': str(discount),
                    'info': str(product.info),
                }
            if price:
                # self.cart[product_id][
                #     'color_text'] = product.product_id.get_color_text_display(
                #     ),
                self.cart[product_id]['price'] = float(price)
                self.cart[product_id]['price_netto'] = round(
                    float(price) / float("1." + "23"), 2)
                self.cart[product_id]['t_netto'] = round(
                    ((float(self.cart[product_id]['price_netto'])) *
                     int(quantity)), 2)
                self.cart[product_id]['t_brutto'] = round(
                    ((float(price)) * int(quantity)), 2)
            if discount:
                self.cart[product_id]['discount'] = float(discount)
            if update_quantity:
                self.cart[product_id]['quantity'] = int(quantity)
            else:
                self.cart[product_id]['quantity'] += int(quantity)
            if info:
                self.cart[product_id]['info'] = info
            self.save()

    def remove(self, product):
        """
        Usuwanie produktu z koszyka
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price_netto(self):
        """
        Obliczanie wartości koszyka wraz z rabatem
        """

        # item['price'] = (((100 - item['discount']) / 100) +
        #                  item['extra_price'])
        _sum = sum((float(item['price_netto']) *
                    (float((100 - float(item['discount'])) / 100)) *
                    int(item['quantity'])) for item in self.cart.values())
        return round(float(_sum), 2)

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
            product_serial = ProductCopySerializer(product)
            cart[str(product.id)]['product'] = product_serial.data
            # cart[str(product.id)]['product'] = product

        for item in cart.values():
            # item['image'] = str(item['product']['image']).replace(
            #     '/media', '')
            image = (item['product']['product_id']['image']).replace(
                '/media/', '')
            item['image'] = image
            item['price'] = round(float(item['price']), 2)
            item['price_netto'] = round(
                float(item['price'] / float("1." + "23")), 2)
            item['discount'] = int(item['discount'])
            # item['total_price'] = int(item['quantity']) * (
            #     (item['price'] * (100 - item['discount'] / 100)))
            item['total_price_netto'] = round(
                float(int(item['quantity']) * float((item['price_netto']))), 2)
            item['total_price'] = round(
                float(int(item['quantity']) * float((item['price']))), 2)
            yield item

    def len(self):
        """
        Obliczanie sumy elementów w koszyku
        """
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session.modified = True

    def clear(self):
        """Usunięcie koszyka z sesji"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
