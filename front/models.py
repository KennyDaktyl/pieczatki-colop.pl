from django.db import models

# Create your models here.


class Pages(models.Model):
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
