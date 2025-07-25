from django.shortcuts import render
from django.views.generic import ListView

from events.repository_impl import EventRepositoryImpl

from .models import Event


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return EventRepositoryImpl(Event).get_all_events()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = self.get_queryset()
        return context
