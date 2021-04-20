from django.contrib import messages
from .models import Orders
import stripe

def new_number(store_id, year, month, day):
    try:
        last_number = Orders.objects.filter(store_id=store_id).first()
        if last_number:
            number_indx = int(last_number.number[:3]) + 1
            ln_day = last_number.date.day
            if ln_day != day:
                number_indx = 1
            if number_indx < 10:
                if day > 9:
                    number_format = f"00{number_indx}/{day}/{month}/{year}"
                else:
                    number_format = f"00{number_indx}/0{day}/{month}/{year}"
            if 100 > number_indx > 9:
                if day > 9:
                    number_format = f"0{number_indx}/{day}/{month}/{year}"
                else:
                    number_format = f"0{number_indx}/0{day}/{month}/{year}"
            if 999 > number_indx > 99:
                if day > 9:
                    number_format = f"{number_indx}/{day}/{month}/{year}"
                else:
                    number_format = f"{number_indx}/0{day}/{month}/{year}"
            if number_indx > 999:
                if day > 9:
                    number_format = f"{number_indx}/{day}/{month}/{year}"
                else:
                    number_format = f"{number_indx}/0{day}/{month}/{year}"
        else:
            number_format = f"001/{day}/{month}/{year}"
        return number_format
    except Orders.DoesNotExist:
        number_format = f"001/{day}/{month}/{year}"
        return number_format

def session_create_stripe();
    stripe.checkout.Session.create(
        payment_method_types=['card', 'p24',],line_items=[{
        'price_data': {
        'currency': 'pln',
        'product_data': {
        'name': 'T-shirt',
      },
      'unit_amount': 2000,
    },
    'quantity': 1,
  }], mode='payment', success_url='https://example.com/success', cancel_url='https://example.com/cancel')
