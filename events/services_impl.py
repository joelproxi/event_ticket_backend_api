
from events.repository_impl import EventRepositoryImpl
from events.services import EventService


class EventServiceImpl(EventService):
    def __init__(self, repository: EventRepositoryImpl):
        self.repository = repository
        
    def get_all_events(self):
        return self.repository.get_all_events()

    def get_events_by_organizer(self, organizer_id: int):
        return self.repository.get_events_by_organizer(organizer_id)

    def create_event(self, **kwargs):
        return self.repository.create_event(**kwargs)

    def get_event(self, event_id: int):
        return self.repository.get_event(event_id)

    def update_event(self, event_id: int, **kwargs):
        return self.repository.update_event(event_id, **kwargs)

    def delete_event(self, event_id: int):
        return self.repository.delete_event(event_id)
