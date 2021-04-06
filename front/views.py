from django.views import View
from django.shortcuts import render, redirect
# from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.conf import settings

from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

from .forms import ContactForm
from .models import Pages
from products.models import Category


class WelcomeView(View):
    def get(self, request):
        page = Pages.objects.get(name='Strona główna')
        categorys = Category.objects.filter(on_page=True)
        ctx = {'page': page, 'categorys': categorys}
        return render(request, "front/welcome.html", ctx)


class ContactView(View):
    def get(self, request):
        site = str(Site.objects.get(pk=get_current_site(request).id))
        # scheme = request.scheme
        scheme = 'https'
        link = scheme + "://" + site + "/kontakt-z-nami/"
        contact_form = ContactForm()
        ctx = {'link': link, 'contact_form': contact_form}

        return render(request, "front/contact.html", ctx)

    def post(self, request):
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            email = request.POST.get("email")
            subject = request.POST.get("subject")
            message = request.POST.get("message")
            captcha = request.POST.get("captcha")

            message += "\n" + "Email kontaktowy - " + str(email)
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [
                    settings.EMAIL_HOST_USER,
                ],
            )
            messages.success(request, 'Wysyłanie email zakończnono poprawnie.')
            return redirect('contact_view')
        else:
            messages.error(request, 'Wypełnij wszystkie pola formularza.')
            return redirect('contact_view', )