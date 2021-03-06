# Generated by Django 3.1.7 on 2021-04-14 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20210412_1232'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryMethod',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.IntegerField(verbose_name='Numer wyświetlania')),
                ('name', models.CharField(max_length=64, verbose_name='Nazwa metody płatności')),
                ('is_active', models.BooleanField(default=True, verbose_name='Czy aktualna')),
            ],
            options={
                'verbose_name_plural': 'Rodzaje dostawy',
                'ordering': ('number',),
            },
        ),
        migrations.AlterModelOptions(
            name='productcopy',
            options={'ordering': ('-id',), 'verbose_name_plural': 'Pozycje rachunku'},
        ),
        migrations.AlterField(
            model_name='productcopy',
            name='order_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.orders', verbose_name='Relacja do zamówienia'),
        ),
    ]
