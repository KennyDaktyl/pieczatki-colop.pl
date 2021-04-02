from django import forms
from crispy_forms.helper import FormHelper
from captcha.fields import ReCaptchaField


class ContactForm(forms.Form):
    helper = FormHelper()
    email = forms.EmailField(
        label="Podaj swój email kontaktowy",
        widget=forms.EmailInput(
            attrs={'placeholder': 'kowalski.janusz@gmail.com'}),
        required=True,
    )
    subject = forms.CharField(
        label="Temat wiadomości",
        widget=forms.TextInput(
            attrs={'placeholder': 'Opinia na temat pizzy'}),
        required=True,
    )
    message = forms.CharField(
        label="Treść wiadomości",
        widget=forms.Textarea(),
        required=True,
    )

    captcha = ReCaptchaField(required=True)
