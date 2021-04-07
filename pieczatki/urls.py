from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from front.sitemaps import *

sitemaps = {
    # 'posts_list': PostSiteView,
    # 'post_details': PostDetailsSiteView,
    # 'blogs_list': BlogDetailsSiteView,
    # 'blog_details': BlogDetailsSiteView,
    # 'workplace_details': WorkplaceSiteView,
    # 'product_details_front': ProductSiteView,
    # 'promo_details': PromoSiteView,
    'static': StaticViewSiteMap,
}

urlpatterns = [
    path('sitemap.xml',
         sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    # url(r"^accounts/", include("django.contrib.auth.urls")),
    path('account/', include('account.urls')),
    path('', include('front.urls')),
    # path('produkty', include('products.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
