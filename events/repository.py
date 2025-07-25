from abc import ABC, abstractmethod
from django.db.models import Count


class EventRepository(ABC):
    @abstractmethod
    def get_all_events(self):
        pass

    def get_events_by_organizer(self, organizer_id: int):
        raise NotImplementedError("This method should be implemented by subclasses")
    
    @abstractmethod
    def create_event(self, **kwargs):
        pass

    @abstractmethod
    def get_event(self, event_id: int):
        pass

    @abstractmethod
    def update_event(self, event_id: int, **kwargs):
        pass
    
    @abstractmethod
    def delete_event(self, event_id):
        pass