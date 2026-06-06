import json
from pathlib import Path
from src.api.services.external.transit import TransitApi
from src.api.services.broadcaster import DeparturesBroadcaster

transit_api: TransitApi | None = None
departures_broadcaster = DeparturesBroadcaster()
STOP_JSON_PATH = Path(__file__).resolve().parents[2] / "data/stops.json"
GLOBAL_STOP_ID_MAPPING: dict[int, str] = {}
stops: set[int] = set()


def load_available_stops():
    global GLOBAL_STOP_ID_MAPPING
    raw_stops = json.loads(STOP_JSON_PATH.read_text())
    for stop in raw_stops['stops']:
        GLOBAL_STOP_ID_MAPPING[stop['stop_id']] = stop['global_stop_id']

def get_transit_api() -> TransitApi:
    if transit_api is None:
        raise RuntimeError("TransitApi is not initialized!")
    return transit_api

if __name__ == "__main__":
    load_available_stops()
    print(stops)
 
