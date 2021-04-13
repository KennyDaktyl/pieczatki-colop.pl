from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import AddProduct, EditQtyProduct, RemoveProduct, CartDetails

# CartDetails,
urlpatterns = [
    path('dodaj_produkt/', AddProduct.as_view(), name='add_products'),
    path('zmien_ilosc/', EditQtyProduct.as_view(), name='change_qty'),
    path('usun_produkt/', RemoveProduct.as_view(), name='del_product'),
    path('podsumowanie/', CartDetails.as_view(), name='cart_details'),
]
