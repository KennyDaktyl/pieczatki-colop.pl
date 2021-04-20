import stripe
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

stripe.api_key = 'sk_test_51IhEZaIs63SrMUIijVMnqrGqnKdsUMAEbrW8S6HcVXKV9kcqQaLHQgBAwcPbi2npi6KPNPuhnHu38AjuaYEMhR1e00hx2DhSpM'

from django.http import HttpResponse


@csrf_protect
def my_webhook_view(request):
    payload = request.body

    # For now, you only need to print out the webhook payload so you can see
    # the structure.
    print(payload)

    return HttpResponse(status=200)


my_webhook_view(request)