import asyncio
from logging import getLogger
from src.api.schemas.stop_departures import StopDeparturesResponse
from src.api.services.external.transit import TransitApi


logger = getLogger(__name__)

class DeparturesBroadcaster:
    def __init__(self):
        self.latest_departures: StopDeparturesResponse | None = None
        self._subscribers: list[asyncio.Event] = []

    def subscribe(self):
        logger.info("New subscriber...")
        event = asyncio.Event() # new client
        if self.latest_departures is not None: # if we have data, it's ready so send it!
            logger.info("Sending latest snapshot.")
            event.set()
        self._subscribers.append(event) # add it to our list of subscribers
        return event

    def _publish(self, data: StopDeparturesResponse):
        logger.info("Updating latest snapshot.")
        self.latest_departures = data
        for event in self._subscribers:
            event.set()

    def unsubscribe(self, event: asyncio.Event):
        logger.info("Unsubcribing...")
        self._subscribers.remove(event)

    async def start(self, api: TransitApi, global_stop_ids: str):
        logger.info("Starting get_stop_departures task.")
        while True:
            try:
                data = await api.get_stop_departures(global_stop_ids)
                self._publish(data)
            except Exception:
                logger.exception("Failed to fetch departures")
            await asyncio.sleep(300)
