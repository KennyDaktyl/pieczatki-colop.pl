import re
from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from crispy_forms.helper import FormHelper
from django.core.validators import validate_email

from .models import Profile
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


class LoginForm(forms.Form):
    username = forms.CharField(label="Login", required=True)

    password = forms.CharField(label="Hasło",
                               widget=forms.PasswordInput,
                               required=True)


class UserForm(forms.ModelForm):
    username = forms.CharField(label="Login",
                               min_length=6,
                               help_text="Minimum 6 znaków",
                               required=True)
    first_name = forms.CharField(label="Imię", required=True)
    last_name = forms.CharField(label="Nazwisko", required=True)

    password = forms.CharField(label="Hasło",
                               widget=forms.PasswordInput,
                               min_length=6,
                               help_text="Minimum 6 znaków",
                               required=True)
    password2 = forms.CharField(label="Powtórz hasło",
                                widget=forms.PasswordInput,
                                min_length=6,
                                required=True)

    email = forms.EmailField(label="email",
                             widget=forms.EmailInput,
                             validators=[validate_email],
                             required=True)

    # is_active = forms.BooleanField(
    #     help_text="Czy użytkownik jest aktywny? (Odznacz zamiast kasować)")

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Hasła nie są identyczne.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError('Zły format email.')

        return email


class PasswordChangeForm(forms.Form):
    password = forms.CharField(label="Hasło",
                               widget=forms.PasswordInput,
                               min_length=6,
                               help_text="Minimum 6 znaków",
                               required=True)
    password2 = forms.CharField(label="Powtórz hasło",
                                widget=forms.PasswordInput,
                                min_length=6,
                                required=True)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Hasła nie są identyczne.')
        return cd['password2']


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email')
