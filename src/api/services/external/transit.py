import asyncio
import os
from typing import Any
from pprint import pprint
from dotenv import load_dotenv
from src.api.schemas import StopDeparturesResponse, SearchStopsResponse

import httpx

BASE_URL = "https://external.transitapp.com"

class TransitApi:
    def __init__(self, api_key: str | None = None):
        self._api_key = api_key or os.environ["TRANSIT_API_KEY"]
        self._client = httpx.AsyncClient(
            base_url=BASE_URL,
            headers={"apiKey": self._api_key},
        )

    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self.close()

    async def _get(self, path: str, params: dict[str, Any]) -> Any:
        clean_params = {k: v for k, v in params.items() if v is not None}
        response = await self._client.get(path, params=clean_params)
        response.raise_for_status()
        return response.json()

    async def get_stop_departures(
        self,
        global_stop_ids: str,
        *,
        time: int | None = None,
        remove_cancelled: bool = False,
        should_update_realtime: bool = True,
        max_num_departures: int = 3,
        include_stops_and_shapes: bool = False,
    ) -> StopDeparturesResponse:
        """GET /v4/public/stop_departures — upcoming departures for one or more stops."""
        response = await self._get(
            "/v4/public/stop_departures",
            {
                "global_stop_ids": global_stop_ids,
                "time": time,
                "remove_cancelled": remove_cancelled,
                "should_update_realtime": should_update_realtime,
                "max_num_departures": max_num_departures,
                "include_stops_and_shapes": include_stops_and_shapes,
            },
        )
        return StopDeparturesResponse.model_validate(response)


    async def search_stops(
        self,
        stop_id: str,
        *,
        lat: float,
        lon: float,
    ) -> SearchStopsResponse:
        """GET /v4/public/search_stops — search stops by name or code."""
        response = await self._get(
            "/v4/public/search_stops",
            {
                "query": stop_id,
                "lat": lat,
                "lon": lon
            },
        )
        return SearchStopsResponse.model_validate(response)

__all__ = ["TransitApi"]

async def test():
    async with TransitApi() as api:
        # res = await api.get_stop_departures("TSL:71358")
        res = await api.search_stops("61701", lat=49, lon=-123)
        pprint(res)

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(test())
