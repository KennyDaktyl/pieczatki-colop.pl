from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import OrderDetails, CheckOutDetails

# CartDetails,
urlpatterns = [
    path('podsumowanie/', OrderDetails.as_view(), name='order_details'),
    path('platnosci/', CheckOutDetails.as_view(), name='checkout_details'),
]
