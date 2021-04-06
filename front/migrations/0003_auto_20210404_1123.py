# Generated by Django 3.1.7 on 2021-04-04 11:23

from django.db import migrations
import django_resized.forms
import front.models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0002_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='WEBP', keep_meta=True, quality=100, size=[1280, 960], upload_to='images/', validators=[front.models.file_size]),
        ),
    ]
