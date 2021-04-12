from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import AddProduct

# CartDetails,
urlpatterns = [
    path('dodaj_produkt/', AddProduct.as_view(), name='add_products'),
    # path('podsumowanie/', CartDetails.as_view(), name='cart_details'),
]
