# Generated by Django 3.1.7 on 2021-04-14 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20210414_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymethod',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7, verbose_name='Cena zamówienia'),
        ),
    ]