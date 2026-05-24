from pydantic import BaseModel

from .service_alert import ServiceAlert
from .display_short_name import DisplayShortName
from .fare import Fare
from .vehicle import Vehicle
from .merged_itinerary import MergedItinerary


class RouteDeparture(BaseModel):
    global_route_id: str
    route_long_name: str
    route_short_name: str
    global_stop_id: str
    merged_itineraries: list[MergedItinerary]
    alerts: list[ServiceAlert] = []
    route_timezone: str | None = None
    route_display_short_name: DisplayShortName | None = None
    compact_display_short_name: DisplayShortName | None = None
    fares: list[Fare] = []
    route_type: int | None = None
    route_color: str | None = None
    route_text_color: str | None = None
    route_network_name: str | None = None
    route_network_id: str | None = None
    tts_long_name: str | None = None
    tts_short_name: str | None = None
    sorting_key: str | None = None
    mode_name: str | None = None
    real_time_route_id: str | None = None
    vehicle: Vehicle | None = None
