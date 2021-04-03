from django.contrib.auth import logout
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LoginView, Logout
# from django.conf import settings
# from django.conf.urls.static import static
# from django.conf.urls import url

urlpatterns = [
    #     path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    #     path('change_user_password/<int:pk>',
    #          ChangeOnlyPasswordView.as_view(),
    #          name='change_only_password'),
]
