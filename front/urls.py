from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import WelcomeView, ProductsListView, ContactView, \
    ProductDetailsView,CategoryDetailsView
from .sitemaps import *

sitemaps = {
    # 'posts_list': PostSiteView,
    # 'post_details': PostDetailsSiteView,
    # 'blogs_list': BlogDetailsSiteView,
    # 'blog_details': BlogDetailsSiteView,
    'category_details': CategorySiteView,
    'product_details_front': ProductSiteView,
    # 'promo_details': PromoSiteView,
    'static': StaticViewSiteMap,
}
urlpatterns = [
    path('', WelcomeView.as_view(), name='welcome'),
    path('produkty/', ProductsListView.as_view(), name='products_list'),
    path(
        'produkty/<slug:category>/<slug:product>/<slug:color>/<slug:store>/<int:pk>/',
        ProductDetailsView.as_view(),
        name='product_details'),
    path('produkty/<slug:category>/<int:pk>/',
         CategoryDetailsView.as_view(),
         name='category_details'),
    path('kontakt-z-nami/', ContactView.as_view(), name='contact_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
