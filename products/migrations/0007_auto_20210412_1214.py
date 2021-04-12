# Generated by Django 3.1.7 on 2021-04-12 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20210409_1259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='size',
        ),
        migrations.AddField(
            model_name='products',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.size', verbose_name='Rozmiar'),
        ),
    ]