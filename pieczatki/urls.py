from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r"^accounts/", include("django.contrib.auth.urls")),
    path('account/', include('account.urls')),
    path('', include('front.urls')),
    path('produkty', include('products.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
