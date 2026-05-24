from pydantic import BaseModel

from .transit import RouteDeparture


class StopDeparturesResponse(BaseModel):
    route_departures: list[RouteDeparture] = []

    def __repr__(self):
        return self.model_dump_json(indent=2)

__all__ = ["StopDeparturesResponse"]
