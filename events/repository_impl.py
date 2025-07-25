from abc import ABC, abstractmethod
from django.db.models import Count

from events.repository import EventRepository


class EventRepositoryImpl(EventRepository):
    def __init__(self, model):
        self.model = model

    def get_all_events(self):
        qs = self.model.objects.annotate(ticket_count=Count('ticket'))
        return qs.select_related('organizer').all()

    def get_events_by_organizer(self, organizer_id: int):
        qs = self.model.objects.annotate(ticket_count=Count('ticket'))
        return qs.filter(organizer_id=organizer_id).select_related('organizer')

    def create_event(self, **kwargs):
        event = self.model(**kwargs)
        event.save()
        return event

    def get_event(self, event_id: int):
        return self.model.objects.get(id=event_id)

    def update_event(self, event_id: int, **kwargs):
        event = self.get_event(event_id)
        for key, value in kwargs.items():
            setattr(event, key, value)
        event.save()
        return event
    
    def delete_event(self, event_id):
        event = self.get_event(event_id)
        event.delete()