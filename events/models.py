from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _



User = get_user_model()


class Organizer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='organizer',
        verbose_name=_("Organizer User")
    )
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
        

class Ticket(models.Model):
    VIP = 'VIP'
    REGULAR = 'REG'
    TICKET_TYPE_CHOICES = [
        (VIP, _("VIP")),
        (REGULAR, _("Regular")),
    ]
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name=_("Event")
    )
    ticket_type = models.CharField(
        max_length=50,
        verbose_name=_("Ticket Type"),
        choices=TICKET_TYPE_CHOICES,
        default=REGULAR
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Ticket Price"))
    available_quantity = models.PositiveIntegerField(verbose_name=_("Available Quantity"))
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket_type} - {self.event.title}"
    
    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")
        indexes = [
            models.Index(fields=['event', 'ticket_type'], name='ticket_event_type_idx'),
            models.Index(fields=['price'], name='ticket_price_idx'),
            models.Index(fields=['available_quantity'], name='ticket_quantity_idx'),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(available_quantity__gte=0),
                name='available_quantity_non_negative'
            ),

        ]