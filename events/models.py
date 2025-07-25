from django.db import models
from django.utils.translation import gettext_lazy as _


class Organizer(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Organizer Name"))
    address = models.CharField(max_length=255, verbose_name=_("Organizer Address"))

    def __str__(self):
        return self.name