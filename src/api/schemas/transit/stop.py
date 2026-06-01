from typing import Literal
from pydantic import BaseModel

from .parent_station import ParentStation


class Stop(BaseModel):
    global_stop_id: str
    location_type: float
    stop_lat: float
    stop_lon: float
    stop_name: str
    distance: float | None = None
    route_type: int | None = None
    stop_code: str | None = None
    rt_stop_id: str | None = None
    wheelchair_boarding: Literal[0, 1, 2] | None = None
    parent_station: ParentStation | None = None

class StopWithStopId(Stop):
    stop_id: str
