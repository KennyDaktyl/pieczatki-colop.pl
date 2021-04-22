from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import OrderDetails, CheckOutDetails, InpostBoxSearchView

# CartDetails,
urlpatterns = [
    path('podsumowanie/', OrderDetails.as_view(), name='order_details'),
    path('podsumowanie/wybierz_paczkomat/',
         InpostBoxSearchView.as_view(),
         name='inpost_box'),
    path('platnosci/<int:order>/',
         CheckOutDetails.as_view(),
         name='checkout_details'),
]
