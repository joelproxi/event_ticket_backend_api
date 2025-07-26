from django.contrib import admin

from events.models import Event, Ticket, Organizer

# Register your models here.
admin.site.register([Event, Ticket, Organizer])
