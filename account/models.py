from django.db import models
from django.db.models import Aggregate, Sum
from django.conf import settings

from datetime import datetime


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    phone_number = models.CharField(verbose_name="Numer telefonu",
                                    max_length=18)

    nip_number = models.CharField(
        verbose_name="Numer nip",
        max_length=13,
        null=True,
        blank=True,
    )
    business_name = models.CharField(
        verbose_name="Nazwa firmy",
        max_length=128,
        null=True,
        blank=True,
    )
    business_name_l = models.CharField(
        verbose_name="Nazwa firmy c.d.",
        max_length=128,
        null=True,
        blank=True,
    )
    company = models.BooleanField(verbose_name="Profil firmowy?",
                                  default=False)

    class Meta:
        ordering = ("user", )
        verbose_name_plural = "Profil użytkownika"

    def __str__(self):
        return "{}, {}, {}".format(self.user.username, self.user.first_name,
                                   self.user.last_name)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        verbose_name="Użytkownik",
        on_delete=models.CASCADE,
    )
    street = models.CharField(verbose_name="Ulica", max_length=128)
    house = models.CharField(verbose_name="Nr domu", max_length=8)
    door = models.CharField(verbose_name="Nr lokalu",
                            null=True,
                            blank=True,
                            max_length=8)
    city = models.CharField(verbose_name="Miasto", max_length=64)
    post_code = models.CharField(verbose_name="Kod pocztowy",
                                 null=True,
                                 blank=True,
                                 max_length=6)

    class Meta:
        ordering = (
            "user_id",
            "-id",
        )
        verbose_name_plural = "Adresy"

    def __str__(self):
        return "{}, {}, {}".format(self.user_id, self.street, self.house)
