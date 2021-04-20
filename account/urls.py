from django.contrib.auth import logout
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LoginView, Logout, AddClientFromBasketView, \
     AddBusinessClientFromBasketView, ChoiceAccountReqisterView, \
          AddAddressBasketView, UpdateAddressBasketView, DeleteAddressBasketView
# from django.conf import settings
# from django.conf.urls.static import static
# from django.conf.urls import url

urlpatterns = [
    #     path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('wybor_konta/',
         ChoiceAccountReqisterView.as_view(),
         name='choice_register'),
    path('rejestracja_klienta_koszyk/',
         AddClientFromBasketView.as_view(),
         name='register_user_basket'),
    path('rejestracja_klienta_biznesowego_koszyk/',
         AddBusinessClientFromBasketView.as_view(),
         name='register_bisness_user_basket'),
    path('dodaj_adres_koszyk/',
         AddAddressBasketView.as_view(),
         name='add_address_basket'),
    path('edytuj_adres_koszyk/<int:pk>/',
         UpdateAddressBasketView.as_view(),
         name='edit_address_basket'),
    path('usun_adres_koszyk/<int:pk>/',
         DeleteAddressBasketView.as_view(),
         name='delete_address_basket'),
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
