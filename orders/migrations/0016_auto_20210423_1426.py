# Generated by Django 3.1.7 on 2021-04-23 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_deliverymethod_id_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='type_of_order',
            new_name='delivery_method',
        ),
        migrations.AddField(
            model_name='orders',
            name='inpost_box',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Numer paczkomatu'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='pay_method',
            field=models.CharField(default=1, max_length=64, verbose_name='Rodzaj płatności'),
            preserve_default=False,
        ),
    ]