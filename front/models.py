from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.core.exceptions import ValidationError
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your models here.
# from tinymce.models import HTMLField


def file_size(value):
    limit = 3 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(
            'Plik który chcesz wrzucić jest większy niż 3MB.')


class Pages(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name="Nazwa strony",
        max_length=13,
    )

    description = models.CharField(
        verbose_name="Meta description",
        max_length=156,
    )

    title = models.CharField(
        verbose_name="Title",
        max_length=70,
    )

    class Meta:
        ordering = ("name", )
        verbose_name_plural = "Strony/Zakładki"

    def __str__(self):
        return "{}".format(self.name)


class Images(models.Model):
    id = models.AutoField(primary_key=True)
    image = ResizedImageField(size=[1280, 960],
                              upload_to='images/',
                              validators=[file_size])
    # product = models.ForeignKey("products.Products",
    #                             on_delete=models.CASCADE,
    #                             blank=True,
    #                             null=True,
    #                             related_name='product_gallery')
    # post = models.ForeignKey("Post",
    #                          on_delete=models.CASCADE,
    #                          blank=True,
    #                          null=True,
    #                          related_name='post_gallery')
    carousel_images = models.BooleanField(verbose_name="Zjęcie dla karulseli?",
                                          default=False)

    class Meta:
        ordering = (
            '-id',
            "image",
        )
        verbose_name_plural = "Galeria"

    def save(self):
        im = Image.open(self.image)
        output = BytesIO()
        im.save(output, format='WEBP', quality=100)
        output.seek(0)
        self.image = InMemoryUploadedFile(
            output, 'ImageField', "%s.webp" % self.image.name.split('.')[0],
            'image/webp', sys.getsizeof(output), None)
        super(Images, self).save()

    def __str__(self):
        return str(self.id)
