from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from src.api import context
from src.api.context import GLOBAL_STOP_ID_MAPPING
from src.api.schemas.stop_departures import StopDeparturesResponse

departures_router = APIRouter(prefix='/departures', tags=['stops'])


@departures_router.get('/')
async def get_departures(stop_id: int) -> StopDeparturesResponse:
    if stop_id not in GLOBAL_STOP_ID_MAPPING:
        raise HTTPException(status_code=404, detail="Stop not found!")
    if context.departures_broadcaster.latest_departures is None:
        raise HTTPException(status_code=503, detail="Departures not yet available")
    global_id = GLOBAL_STOP_ID_MAPPING[stop_id]
    filtered = [r for r in context.departures_broadcaster.latest_departures.route_departures
                if r.global_stop_id == global_id]
    return StopDeparturesResponse(route_departures=filtered)


# @departures_router.get('/all')
# async def get_all_departures(request: Request):
#     event = context.departures_broadcaster.subscribe()
#
#     async def event_generator():
#         try:
#             while not await request.is_disconnected():
#                 await event.wait()
#                 event.clear()
#                 yield f"data: {context.departures_broadcaster.latest_departures.model_dump_json()}\n\n"
#         finally:
#             context.departures_broadcaster.unsubscribe(event)
#
#     return StreamingResponse(
#         event_generator(),
#         media_type="text/event-stream",
#         headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
#     )


__all__ = ["departures_router"]
