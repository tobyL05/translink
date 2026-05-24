from pydantic import BaseModel


class InformedEntity(BaseModel):
    global_route_id: str | None = None
    global_stop_id: str | None = None
    rt_trip_id: str | None = None
