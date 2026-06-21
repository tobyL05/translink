from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
from dotenv import load_dotenv
import os
import json
import httpx
from pprint import pprint

BASE_URL = "https://gtfsapi.translink.ca/v3/gtfsposition?apikey="

load_dotenv()


def fetch_and_save():
    feed = gtfs_realtime_pb2.FeedMessage()  # type: ignore[attr-defined]
    response = httpx.get(BASE_URL + os.environ["TRANSLINK_API_KEY"])
    feed.ParseFromString(response.content)
    vehicles = [
        MessageToDict(entity.vehicle)
        for entity in feed.entity
        if entity.HasField("vehicle")
    ]

    with open("gtfs_output.json", "w") as f:
        json.dump(vehicles, f, indent=2)


def parse_output():
    with open("gtfs_output.json", "r") as f:
        output = json.load(f)
        for vehicle in output:
            print(vehicle["trip"]["tripId"])
            if vehicle["trip"]["tripId"] == "15271976":
                pprint(vehicle)


if __name__ == "__main__":
    fetch_and_save()
    parse_output()
