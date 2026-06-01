from fastapi import APIRouter, HTTPException, Depends
from src.api.context import GLOBAL_STOP_ID_MAPPING, get_transit_api
from src.api.schemas.stop_departures import StopDeparturesResponse
from src.api.services.external import TransitApi

departures_router = APIRouter(prefix='/departures', tags=['stops'])

@departures_router.get('/')
async def get_departures(
        stop_id: int,
        transit_api: TransitApi = Depends(get_transit_api)) -> StopDeparturesResponse:
    if stop_id not in GLOBAL_STOP_ID_MAPPING:
        raise HTTPException(status_code=404, detail="Stop not found!")
    return await transit_api.get_stop_departures(GLOBAL_STOP_ID_MAPPING[stop_id])


__all__ = ["departures_router"]
