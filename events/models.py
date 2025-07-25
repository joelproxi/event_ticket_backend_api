from django.db import models
from django.utils.translation import gettext_lazy as _


class Organizer(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Organizer Name"))
    address = models.CharField(max_length=255, verbose_name=_("Organizer Address"))

    def __str__(self):
        return self.name
    
    
class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Event Title"))
    description = models.TextField(verbose_name=_("Event Description"))
    start_date = models.DateTimeField(verbose_name=_("Event Date"))
    end_date = models.DateTimeField(verbose_name=_("Event End Date"))
    location = models.CharField(max_length=255, verbose_name=_("Event Location"))
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='events', verbose_name=_("Organizer"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ['start_date']
        indexes = [
            models.Index(fields=['start_date'], name='event_start_date_idx'),
            models.Index(fields=['end_date'], name='event_end_date_idx'),
        ]
        constraints = [
            # models.CheckConstraint(
            #     check=models.Q(start_date__lt=models.F('end_date')),
            #     name='start_date_before_end_date'
            # )
            models.UniqueConstraint(
                fields=['title', 'start_date'],
                name='unique_event_title_start_date'
            )
        ]