from typing import Literal
from pydantic import BaseModel


class ScheduleItem(BaseModel):
    departure_time: float
    arrival_time: float
    is_cancelled: bool
    is_real_time: bool
    scheduled_departure_time: float
    scheduled_arrival_time: float
    rt_trip_id: str | None = None
    wheelchair_accessible: Literal[0, 1, 2] | None = None
    trip_search_key: str | None = None


class ScheduleItemWithInternalId(ScheduleItem):
    internal_itinerary_id: str
    is_last: bool | None = None
