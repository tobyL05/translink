import argparse
import asyncio
import json
from pathlib import Path

from dotenv import load_dotenv
from src.api.services import TransitApi

STOPS_FILE = Path(__file__).parent.parent / "data" / "stops.json"


def load_stops() -> list[dict]:
    if not STOPS_FILE.exists():
        return []
    data = json.loads(STOPS_FILE.read_text())
    return data.get("stops", [])


def save_stops(stops: list[dict]) -> None:
    STOPS_FILE.write_text(json.dumps({"stops": stops}, indent=2))


async def add_stops(stop_ids: list[str], lat: float, lon: float) -> None:
    existing = load_stops()
    seen_global_ids = {s["global_stop_id"] for s in existing if s.get("global_stop_id")}

    async with TransitApi() as api:
        for i, stop_id in enumerate(stop_ids):
            if i > 0:
                await asyncio.sleep(5.0)
            response = await api.search_stops(stop_id, lat=lat, lon=lon)

            if not response.results:
                print(f"No results for {stop_id!r}")
                continue

            best = max(response.results, key=lambda r: r.match_strength)

            if best.global_stop_id in seen_global_ids:
                print(f"Already exists: {best.stop_name} ({best.global_stop_id})")
                continue

            entry = {
                "stop_id": int(stop_id) if stop_id.isdigit() else None,
                "stop_name": best.stop_name,
                "global_stop_id": best.global_stop_id,
                "stop_lat": best.stop_lat,
                "stop_lon": best.stop_lon,
                "route_type": best.route_type,
                "location_type": best.location_type,
            }

            # Update an existing placeholder entry if one exists for this stop_id
            placeholder = next(
                (s for s in existing if str(s.get("stop_id")) == stop_id), None
            )
            if placeholder:
                placeholder.update(entry)
            else:
                existing.append(entry)

            seen_global_ids.add(best.global_stop_id)
            print(
                f"Added: {best.stop_name} ({best.global_stop_id}) [match: {best.match_strength:.2f}]"
            )

    save_stops(existing)
    print(f"\nSaved {len(existing)} stops to {STOPS_FILE}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resolve local stop IDs to global stop IDs and save to stops.json"
    )
    parser.add_argument(
        "stop_ids", nargs="+", help="Local stop IDs or names to search for"
    )
    args = parser.parse_args()

    load_dotenv()
    print("adding stops..")
    asyncio.run(add_stops(args.stop_ids, 49, -123))


if __name__ == "__main__":
    print("running..")
    main()
