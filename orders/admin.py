from django.contrib import admin
from .models import PayMethod, DeliveryMethod, Orders, ProductCopy


@admin.register(PayMethod)
class PayMethonAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PayMethod._meta.fields]


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DeliveryMethod._meta.fields]


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Orders._meta.fields]
    list_filter = (
        'store',
        'user',
        'pay_method',
    )
    search_fields = ('number', )


@admin.register(ProductCopy)
class ProductCopyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ProductCopy._meta.fields]
    exclude = ['order']
