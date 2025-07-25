from abc import ABC, abstractmethod
from events.repository_impl import EventRepositoryImpl


class EventService(ABC):
    @abstractmethod
    def get_all_events(self):
       pass
   
    @abstractmethod
    def get_events_by_organizer(self, organizer_id: int):
        pass

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
    def delete_event(self, event_id: int):
        pass