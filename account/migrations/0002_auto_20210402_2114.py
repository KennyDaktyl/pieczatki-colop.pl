# Generated by Django 3.1.7 on 2021-04-02 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ('user_id',), 'verbose_name_plural': 'Adresy'},
        ),
    ]