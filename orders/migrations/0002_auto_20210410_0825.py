# Generated by Django 3.2 on 2021-04-10 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='paymethod',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]