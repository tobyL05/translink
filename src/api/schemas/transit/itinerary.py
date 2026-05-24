from pydantic import BaseModel

from .stop import Stop
from .schedule_item import ScheduleItem


class Itinerary(BaseModel):
    direction_id: float
    headsign: str
    direction_headsign: str | None = None
    merged_headsign: str | None = None
    branch_code: str | None = None
    shape: str | None = None
    canonical_itinerary: bool | None = None
    is_active: bool | None = None
    closest_stop: Stop | None = None
    stops: list[Stop] = []
    schedule_items: list[ScheduleItem] = []


class ItineraryWithInternalId(Itinerary):
    internal_itinerary_id: str
