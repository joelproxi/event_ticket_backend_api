from typing import Any

from django.forms import modelformset_factory
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView

from events.forms import EventForm, TicketForm
from events.repository_impl import EventRepositoryImpl

from .models import Event, Ticket, Organizer
from .services_impl import EventServiceImpl


class EventListView(ListView):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._service =  EventServiceImpl(EventRepositoryImpl(Event))

    template_name = 'events/list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return self._service.get_all_events()

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        context.update({
            'events': self.get_queryset()
        })
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event'


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/form.html'
    success_url = reverse_lazy('event_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_form_set = modelformset_factory(Ticket, form=TicketForm, extra=3, can_delete=True)
        if self.request.POST:
            context['ticket_formset'] = ticket_form_set(data=self.request.POST, queryset=Ticket.objects.none())
        else:
            context['ticket_formset'] = ticket_form_set(queryset=Ticket.objects.none())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ticket_formset = context['ticket_formset']
        if ticket_formset.is_valid():
            organizer = Organizer.objects.first()
            event = form.save(commit=False)
            event.organizer = organizer
            event.save()
            tickets = ticket_formset.save(commit=False)
            for ticket in tickets:
                ticket.event = event
                ticket.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/form.html'
    success_url = reverse_lazy('event_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_form_set = modelformset_factory(Ticket, form=TicketForm, can_delete=True, extra=2)
        if self.request.POST:
            context['ticket_formset'] = ticket_form_set(
                data=self.request.POST, queryset=Ticket.objects.filter(event=self.object))
        else:
            context['ticket_formset'] = ticket_form_set(queryset=Ticket.objects.filter(event=self.object))
        return context

    def form_valid(self, form):

        context = self.get_context_data()
        ticket_formset = context['ticket_formset']
        if ticket_formset.is_valid():
            event = form.save(commit=False)
            tickets = ticket_formset.save(commit=False)
            for ticket in tickets:
                ticket.event = event
                ticket.save()
            for ticket in ticket_formset.deleted_objects:
                ticket.delete()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


