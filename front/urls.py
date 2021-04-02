from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from .views import WelcomeView, ContactView
from .sitemaps import *

# sitemaps = {
#     'posts_list': PostSiteView,
#     'post_details': PostDetailsSiteView,
#     'blogs_list': BlogDetailsSiteView,
#     'blog_details': BlogDetailsSiteView,
#     'workplace_details': WorkplaceSiteView,
#     'product_details_front': ProductSiteView,
#     'promo_details': PromoSiteView,
#     'static': StaticViewSiteMap,
# }
urlpatterns = [
    # path('sitemap.xml',
    #      sitemap, {'sitemaps': sitemaps},
    #      name='django.contrib.sitemaps.views.sitemap'),
    path('', WelcomeView.as_view(), name='welcome'),
    path('kontakt-z-nami/', ContactView.as_view(), name='contact_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
