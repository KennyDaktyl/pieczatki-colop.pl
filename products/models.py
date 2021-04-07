from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from django_resized import ResizedImageField
from django.core.exceptions import ValidationError
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from decimal import Decimal


def file_size(value):
    limit = 3 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(
            'Plik który chcesz wrzucić jest większy niż 3MB.')


class Store(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nazwa magazynu", max_length=64)
    image = ResizedImageField(verbose_name="Zdjęcie główne",
                              size=[1280, 960],
                              null=True,
                              blank=True,
                              upload_to='images/workplace/',
                              validators=[file_size])
    phone_number = models.CharField(
        verbose_name="Telefon kontaktowy do magazynu", max_length=32)
    street = models.CharField(verbose_name="Ulica/Osiedle", max_length=128)
    home = models.CharField(verbose_name="Numer domu", max_length=8)
    door = models.CharField(
        verbose_name="Numer lokalu",
        max_length=8,
        null=True,
        blank=True,
    )
    city = models.CharField(verbose_name="Miasto",
                            max_length=64,
                            default="Kraków")
    post_code = models.CharField(verbose_name="Kod pocztowy",
                                 null=True,
                                 blank=True,
                                 max_length=6)
    info = models.CharField(verbose_name="Info",
                            max_length=256,
                            null=True,
                            blank=True)

    is_active = models.BooleanField(verbose_name="Czy jest aktywna",
                                    default=True)

    slug = models.SlugField(verbose_name="Slug",
                            blank=True,
                            null=True,
                            max_length=128)
    google_maps_link = models.TextField(verbose_name="Link z mapy google",
                                        null=True,
                                        blank=True)
    facebook_link = models.URLField(verbose_name="Link do facebook",
                                    null=True,
                                    blank=True)

    def products(self):
        return Products.objects.filter(store_id=self).filter(is_active=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name + "-" + self.street + "-" + self.home +
                            "-" + self.city)
        super(Store, self).save()

    # def get_absolute_url(self):
    #     return reverse("store_details", kwargs={
    #         "slug": self.slug,
    #     })

    class Meta:
        ordering = ("id", )
        verbose_name_plural = "Magazyn"

    def __str__(self):
        return "{}, {}".format(str(self.id), self.name)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    tag_desc = models.CharField(
        verbose_name="Meta description",
        max_length=156,
    )

    tag_title = models.CharField(
        verbose_name="Title",
        max_length=70,
    )
    number = models.IntegerField(verbose_name="Numer kategorii",
                                 null=True,
                                 blank=True,
                                 default=0)
    image = ResizedImageField(verbose_name="Zdjęcie główne",
                              size=[1280, 960],
                              upload_to='images/categorys/',
                              validators=[file_size],
                              null=True,
                              blank=True)
    alt = models.CharField(
        verbose_name="Alternatywny text dla obrazka",
        max_length=125,
        blank=True,
        null=True,
    )
    title = models.CharField(verbose_name="Title dla obrazka",
                             blank=True,
                             null=True,
                             max_length=70)
    name = models.CharField(verbose_name="Nazwa kategorii", max_length=128)
    text = models.TextField(verbose_name="Opis kategorii")
    slug = models.SlugField(verbose_name="Slug",
                            blank=True,
                            null=True,
                            max_length=128)
    on_page = models.BooleanField(verbose_name="Czy na pierwszej stronie?",
                                  default=False)
    is_active = models.BooleanField(verbose_name="Czy jest dostępny",
                                    default=True)

    def counter(self, workplace):
        return Products.objects.filter(category=self).filter(
            is_active=True).filter(store_id=workplace).count()

    def products(self):
        return Products.objects.filter(category=self).filter(is_active=True)

    def images_stamp(self):
        return Images.objects.filter(category_id=self).filter(stamp=True)

    class Meta:
        ordering = (
            "number",
            "name",
        )
        verbose_name_plural = "Kategorie produktów"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save()

    def __str__(self):
        return self.name


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nazwa marki", max_length=128)
    logo = ResizedImageField(verbose_name="Zdjęcie główne",
                             size=[1280, 960],
                             upload_to='images/categorys/',
                             validators=[file_size],
                             null=True,
                             blank=True)
    alt = models.CharField(
        verbose_name="Alternatywny text dla obrazka",
        max_length=125,
        blank=True,
        null=True,
    )
    title = models.CharField(verbose_name="Title dla obrazka",
                             blank=True,
                             null=True,
                             max_length=70)
    desc = models.TextField(verbose_name="Brand info", blank=True, null=True)

    class Meta:
        ordering = ("name", )
        verbose_name_plural = "Marka produktów"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save()

    def __str__(self):
        return self.name


class Size(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name="Rozmiar produktu (wielkość, pojemność, waga)",
        max_length=64)
    is_active = models.BooleanField(verbose_name="Czy jest aktualny",
                                    default=True)

    def products(self, workplace):
        return Products.objects.filter(size=self).filter(
            is_active=True).filter(store_id=workplace)

    def counter(self, workplace):
        return Products.objects.filter(size=self).filter(
            is_active=True).filter(store_id=workplace).count()

    class Meta:
        ordering = ('name', )
        verbose_name_plural = "Rozmiary produktów"

    def __str__(self):
        return self.name


class Vat(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.IntegerField(verbose_name="Stawka VAT")
    is_active = models.BooleanField(verbose_name="Czy jest dostępny",
                                    default=True)

    def __str__(self):
        return "{}%".format(self.name)


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    store_id = models.ForeignKey("Store",
                                 verbose_name="Magazyn",
                                 on_delete=models.CASCADE,
                                 db_index=True,
                                 default=1)
    category = models.ForeignKey(
        "Category",
        verbose_name="Kategoria produktu",
        on_delete=models.CASCADE,
        db_index=True,
    )
    brand = models.ForeignKey("Brand",
                              verbose_name="Marka produktu",
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)
    name = models.CharField(verbose_name="Nazwa produktu", max_length=128)
    qty = models.IntegerField(default=1,
                              verbose_name="Ilość produktu na stanie")
    size = models.ManyToManyField('Size', verbose_name="Rozmiar", blank=True)
    desc = models.TextField(verbose_name="Produkt info", blank=True, null=True)
    slug = models.SlugField(verbose_name="Slug",
                            blank=True,
                            null=True,
                            max_length=128)
    image = ResizedImageField(verbose_name="Zdjęcie główne",
                              size=[1280, 960],
                              upload_to='images/products/',
                              validators=[file_size],
                              null=True,
                              blank=True)
    alt = models.CharField(
        verbose_name="Alternatywny text dla obrazka",
        max_length=125,
        blank=True,
        null=True,
    )
    title = models.CharField(verbose_name="Title dla obrazka",
                             blank=True,
                             null=True,
                             max_length=70)
    price = models.DecimalField(verbose_name="Cena podstawowa",
                                default=0,
                                decimal_places=2,
                                max_digits=7)
    price_netto = models.DecimalField(verbose_name="Cena podstawowa",
                                      default=0,
                                      decimal_places=2,
                                      max_digits=7,
                                      null=True,
                                      blank=True)
    tax = models.ForeignKey(
        "Vat",
        on_delete=models.CASCADE,
        verbose_name="Stawka VAT",
    )
    is_active = models.BooleanField(verbose_name="Czy jest dostępny",
                                    default=True)

    def images(self):
        return Images.objects.filter(product_id=self)

    def get_absolute_url(self):
        return reverse("product_details_front",
                       kwargs={
                           "magasize": self.workplace_id.slug,
                           "cat": self.sub_category.category.slug,
                           "slug": self.slug,
                           "pk": self.id,
                       })

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.price_netto = self.price / Decimal("1." + str(self.tax.name))
        super(Products, self).save()

    class Meta:
        ordering = ("name", )
        verbose_name_plural = "Produkty"

    def __str__(self):
        return "{} ({})".format(self.name, self.size.name)


class Images(models.Model):
    id = models.AutoField(primary_key=True)
    image = ResizedImageField(size=[1280, 960],
                              upload_to='images/',
                              validators=[file_size])
    alt = models.CharField(
        verbose_name="Alternatywny text dla obrazka",
        max_length=125,
        blank=True,
        null=True,
    )
    title = models.CharField(verbose_name="Title dla obrazka",
                             blank=True,
                             null=True,
                             max_length=70)
    category = models.ForeignKey("Category",
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True,
                                 verbose_name="Zdjęcia kategorii",
                                 related_name='category_gallery')
    product = models.ForeignKey("Products",
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                verbose_name="Zdjęcie produktu",
                                related_name='product_gallery')
    main = models.BooleanField(verbose_name="Zdjęcie główne", default=False)
    stamp = models.BooleanField(verbose_name="Zdjęcie wzornika?",
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