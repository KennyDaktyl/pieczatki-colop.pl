from django.views import View
from django.shortcuts import render, redirect
# from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse

from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ContactForm
from .models import Pages
from products.models import Category, Brand, Products
from products.constants import STAMP_COLORS
from orders.models import ProductCopy
from cart.cart import Cart


class WelcomeView(View):
    def get(self, request):
        page = Pages.objects.get(name='Strona główna')
        categorys = Category.objects.filter(on_page=True)
        logo_colop = Brand.objects.get(name='Colop')
        logo_universal = Brand.objects.get(name='Universal')
        ctx = {
            'page': page,
            'categorys': categorys,
            'logo_colop': logo_colop,
            'logo_universal': logo_universal
        }
        return render(request, "front/welcome.html", ctx)


class ProductsListView(ListView):
    model = Products
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        category = self.request.GET.get('category')
        size = self.request.GET.get('size')
        products = Products.objects.filter(is_active=True)
        categorys = Category.objects.filter(is_active=True)
        if category:
            cat = Category.objects.get(pk=category)
            products = products.filter(category=cat)

        if size:
            products = products.filter(size=size)
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            toppings = paginator.page(page)
        except PageNotAnInteger:
            toppings = paginator.page(1)
        except EmptyPage:
            toppings = paginator.page(paginator.num_pages)
        context['products'] = products
        context['categorys'] = categorys
        context['colors'] = STAMP_COLORS
        return context


class ProductDetailsView(DetailView):
    model = Products

    def get_context_data(self, **kwargs):
        ctx = super(ProductDetailsView, self).get_context_data(**kwargs)
        ctx['categorys'] = Category.objects.filter(is_active=True)
        site = Site.objects.get(pk=get_current_site(self.request).id)
        a_url = self.object.get_absolute_url()
        site = str(Site.objects.get(pk=get_current_site(self.request).id))
        # scheme = request.scheme
        scheme = 'https'
        link = scheme + "://" + site + a_url
        ctx['site'] = site
        ctx['link'] = link
        ctx['cannonical'] = scheme + "://" + site + "/produkty/" + self.object.category.slug + "/" + self.object.slug + "/"
        ctx['colors'] = STAMP_COLORS
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.is_ajax():
            color_s = self.request.POST.get("color_s")
            # prod_id = self.request.POST.get("prod_id")
            qty = self.request.POST.get("qty")
            product = ProductCopy()
            product.product_id = self.object
            product.color_text = color_s
            product.qty = int(qty)
            product.price = self.object.price
            if self.object.price_promo:
                product.price = self.object.price_promo
            product.save()
            Cart.add(Cart, product, product.price, product.discount,
                     product.info, product.qty)
            print(product)
            return HttpResponse(True)
        else:
            return redirect('product_details',
                            category=self.object.category.slug,
                            product=self.object.slug,
                            color=self.object.color.slug,
                            store=self.object.store.slug,
                            pk=self.object.id)


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