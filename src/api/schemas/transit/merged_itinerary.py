from pydantic import BaseModel

from .stop import Stop
from .itinerary import ItineraryWithInternalId
from .schedule_item import ScheduleItemWithInternalId


class MergedItinerary(BaseModel):
    direction_id: int | None = None
    closest_stop: Stop | None = None
    itineraries: list[ItineraryWithInternalId] = []
    schedule_items: list[ScheduleItemWithInternalId] = []
