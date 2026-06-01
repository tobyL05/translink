from pydantic import BaseModel

from .transit import Stop


class SearchStopResult(Stop):
    match_strength: float


class SearchStopsResponse(BaseModel):
    results: list[SearchStopResult] = []

__all__ = ["SearchStopResult", "SearchStopsResponse"]
