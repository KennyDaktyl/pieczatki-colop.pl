from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from front.sitemaps import *

sitemaps = {
    # 'posts_list': PostSiteView,
    # 'post_details': PostDetailsSiteView,
    # 'blogs_list': BlogDetailsSiteView,
    # 'blog_details': BlogDetailsSiteView,
    'category_details': CategorySiteView,
    'product_details': ProductSiteView,
    # 'promo_details': PromoSiteView,
    'static': StaticViewSiteMap,
}

urlpatterns = [
    path('sitemap.xml',
         sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    url(
        r'^robots\.txt$',
        TemplateView.as_view(template_name="front/robots.txt",
                             content_type='text/plain')),
    path('admin/', admin.site.urls),
    # url(r"^accounts/", include("django.contrib.auth.urls")),
    path('konto/', include('account.urls')),
    path('koszyk/', include('cart.urls')),
    path('zamowienia/', include('orders.urls')),
    path('', include('front.urls')),
    # path('produkty', include('products.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
