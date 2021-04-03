from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r"^accounts/", include("django.contrib.auth.urls")),
    path('account/', include('account.urls')),
    path('', include('front.urls')),
]
