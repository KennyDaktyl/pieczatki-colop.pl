# Generated by Django 3.1.7 on 2021-04-04 11:00

from django.db import migrations, models
import django_resized.forms
import front.models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=0, size=[1280, 960], upload_to='images/', validators=[front.models.file_size])),
                ('carousel_images', models.BooleanField(default=False, verbose_name='Zjęcie dla karulseli?')),
            ],
            options={
                'verbose_name_plural': 'Galeria',
                'ordering': ('-id', 'image'),
            },
        ),
    ]
