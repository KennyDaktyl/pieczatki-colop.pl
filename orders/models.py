from django.db import models
from django.db.models import Sum
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings

from decimal import Decimal
from products.constants import STAMP_COLORS, STAMP_COLORS_TEXT
from .constants import PAY_METHOD, ORDER_STATUS, DELIVERY_TYPE


class PayMethod(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(verbose_name="Numer wyświetlania")
    name = models.CharField(verbose_name="Nazwa metody płatności",
                            max_length=64)
    pay_method = models.IntegerField(verbose_name="Rodzaj płatności",
                                     choices=PAY_METHOD)
    price = models.DecimalField(verbose_name="Cena zamówienia",
                                default=0.00,
                                decimal_places=2,
                                max_digits=7)
    default = models.BooleanField(verbose_name="Czy domyślny?", default=False)
    is_active = models.BooleanField(verbose_name="Czy aktualna", default=True)

    def total_income(self, orders):
        orders_in_this_pay_m = orders.filter(pay_method=self)
        orders_realised = orders_in_this_pay_m.filter(status=4)
        pm_income_all_count = orders_in_this_pay_m.count()
        pm_income_closed_count = orders_realised.count()
        if orders_realised.aggregate(Sum('total_price'))['total_price__sum']:
            _sum = orders_realised.aggregate(
                Sum('total_price'))['total_price__sum']
        else:
            _sum = 0.00

        return [self.name, pm_income_all_count, pm_income_closed_count, _sum]

    class Meta:
        ordering = ("number", )
        verbose_name_plural = "Rodzaje płatności"

    def __str__(self):
        return self.name


class DeliveryMethod(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(verbose_name="Numer wyświetlania")
    name = models.CharField(verbose_name="Nazwa metody płatności",
                            max_length=64)
    price = models.DecimalField(verbose_name="Cena za dostawę",
                                default=0.00,
                                decimal_places=2,
                                max_digits=7)
    price_promo = models.DecimalField(verbose_name="Cena promocyjna",
                                      default=0.00,
                                      decimal_places=2,
                                      max_digits=7)
    default = models.BooleanField(verbose_name="Czy domyślny?", default=False)
    is_active = models.BooleanField(verbose_name="Czy aktualna?", default=True)

    class Meta:
        ordering = ("number", )
        verbose_name_plural = "Rodzaje dostawy"

    def __str__(self):
        return self.name


# Pay_Method have to not NONE - order have to get pay_method id
class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(verbose_name="Numer zamówienia", max_length=64)
    status = models.IntegerField(verbose_name="Status zamówienia",
                                 choices=ORDER_STATUS,
                                 default=1)
    date = models.DateTimeField(db_index=True)
    store = models.ForeignKey("products.Store",
                              on_delete=models.CASCADE,
                              verbose_name="Magazyn",
                              db_index=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Osoba rejestrująca zamówienie",
        related_name="profile_id",
    )
    client = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               verbose_name="Klient",
                               related_name="clinet_id",
                               null=True,
                               blank=True)
    type_of_order = models.IntegerField(verbose_name="Rodzaj zamówienia",
                                        choices=DELIVERY_TYPE)

    address = models.ForeignKey("account.Address",
                                on_delete=models.CASCADE,
                                verbose_name="Adres dostawy",
                                null=True,
                                blank=True)
    phone_number = models.CharField(verbose_name="Numer telefonu",
                                    null=True,
                                    blank=True,
                                    max_length=12)
    pay_method = models.ForeignKey("PayMethod",
                                   on_delete=models.CASCADE,
                                   verbose_name="Rodzaj płatności",
                                   null=True,
                                   blank=True)

    start_delivery_time = models.TimeField(verbose_name="Czas wywozu",
                                           blank=True,
                                           null=True)
    sms_send = models.BooleanField(verbose_name="Sms", default=False)
    sms_time = models.TimeField(verbose_name="Czas smsa",
                                blank=True,
                                null=True)
    promo = models.BooleanField(verbose_name="Promocja", default=False)
    discount = models.IntegerField(verbose_name="Rabat", default=0)
    info = models.CharField(verbose_name="Informacje",
                            max_length=256,
                            null=True,
                            blank=True)
    is_paid = models.BooleanField(verbose_name="Czy zapłacono?", default=False)
    printed = models.BooleanField(verbose_name="Wydrukowano paragon?",
                                  default=True)

    total_price = models.DecimalField(verbose_name="Cena zamówienia",
                                      default=0.00,
                                      decimal_places=2,
                                      max_digits=7)

    def orders_closed(self):
        return self.objects.filter(status=5)

    def status_count(self, status):
        return self.objects.filter(status=status).count()

    def positions_on_order(self):
        return ProductCopy.objects.filter(
            order=self).order_by('product').order_by('id')

    def counter_positions(self):
        return ProductCopy.objects.filter(order_id=self).count()

    def total_price_1(self):
        positions_order = ProductCopy.objects.filter(order=self).exclude(
            order=None)
        if positions_order.aggregate(Sum('total_price'))['total_price__sum']:
            _sum = positions_order.aggregate(
                Sum('total_price'))['total_price__sum']
        else:
            _sum = 0.00
        return Decimal(_sum)

    def total_price_2(self):
        total_price = Decimal(self.total_price_1())

        if int(self.discount) > 0:
            return round(
                Decimal(
                    (total_price -
                     (Decimal(total_price) * Decimal(self.discount) / 100))),
                2,
            )
        if int(self.discount) == 0:
            return Decimal(self.total_price_1())

    def save(self, *args, **kwargs):
        self.total_price = self.total_price_2()
        super(Orders, self).save(*args, **kwargs)

    class Meta:
        ordering = ("-id", )
        verbose_name_plural = "Zamówienia"

    def __str__(self):
        return "{}-{}-{}".format(self.number, self.store.name,
                                 self.get_status_display())


class ProductCopy(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey("Orders",
                                 verbose_name="Relacja do zamówienia",
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True)
    product_id = models.ForeignKey("products.Products",
                                   verbose_name="Relacja do produktu",
                                   on_delete=models.CASCADE)
    color_text = models.IntegerField(verbose_name="Kolor odbicia",
                                     choices=STAMP_COLORS)
    qty = models.IntegerField(verbose_name="Ilość pozycji")
    price = models.DecimalField(verbose_name="Cena podstawowa",
                                default=0,
                                decimal_places=2,
                                max_digits=7)
    discount = models.IntegerField(verbose_name="Rabat", default=0)
    info = models.CharField(verbose_name="Informacje",
                            max_length=256,
                            null=True,
                            blank=True)

    class Meta:
        ordering = ("-id", )
        verbose_name_plural = "Pozycje rachunku"

    def __str__(self):
        if self.order_id:
            return "{}, {}".format(str(self.order), self.product.name)
        else:
            return "{}".format(self.product_id.name)