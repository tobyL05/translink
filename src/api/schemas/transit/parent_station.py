from pydantic import BaseModel


class ParentStation(BaseModel):
    global_stop_id: str | None = None
    location_type: str | None = None
    rt_stop_id: str | None = None
    station_code: str | None = None
    station_name: str | None = None
