import csv
import io
import sqlite3
import sys
import argparse
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx

GTFS_DIR = Path(__file__).parent.parent / "google_transit"
DB_PATH = Path(__file__).parent.parent / "gtfs.db"


def _read_stops():
    rows = []
    with open(GTFS_DIR / "stops.txt", newline="") as f:
        for r in csv.DictReader(f):
            try:
                rows.append((int(r["stop_id"]), r["stop_code"], r["stop_name"], float(r["stop_lat"]), float(r["stop_lon"])))
            except (ValueError, KeyError):
                pass
    return rows


def _read_stop_times():
    rows = []
    with open(GTFS_DIR / "stop_times.txt", newline="") as f:
        for r in csv.DictReader(f):
            try:
                rows.append((r["trip_id"], int(r["stop_id"]), int(r["stop_sequence"]), r["arrival_time"], r["departure_time"]))
            except (ValueError, KeyError):
                pass
    return rows


def load(conn: sqlite3.Connection):
    conn.executescript("""
        PRAGMA synchronous = OFF;
        PRAGMA journal_mode = MEMORY;
        CREATE TABLE IF NOT EXISTS stops (
            stop_id   INTEGER PRIMARY KEY,
            stop_code TEXT,
            stop_name TEXT,
            stop_lat  REAL,
            stop_lon  REAL
        );
        CREATE INDEX IF NOT EXISTS idx_stops_code ON stops(stop_code);
        CREATE TABLE IF NOT EXISTS stop_times (
            trip_id        TEXT,
            stop_id        INTEGER,
            stop_sequence  INTEGER,
            arrival_time   TEXT,
            departure_time TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_stop_times_trip ON stop_times(trip_id);
    """)

    print("Reading CSVs...")
    with ThreadPoolExecutor() as executor:
        stops_fut = executor.submit(_read_stops)
        stop_times_fut = executor.submit(_read_stop_times)
        stops = stops_fut.result()
        stop_times = stop_times_fut.result()

    print(stops[0])
    print(stop_times[0])

    print(f"Writing {len(stops)} stops and {len(stop_times)} stop_times...")
    conn.executemany("INSERT OR REPLACE INTO stops VALUES (?,?,?,?,?)", stops)
    conn.executemany("INSERT OR REPLACE INTO stop_times VALUES (?,?,?,?,?)", stop_times)
    conn.commit()
    print(f"Done — {DB_PATH}")


def download():
    url = "https://gtfs-static.translink.ca/gtfs/google_transit.zip"
    print(f"Downloading {url}...")
    try:
        response = httpx.get(url, follow_redirects=True, timeout=30)
        response.raise_for_status()
    except httpx.HTTPError as e:
        print(f"Download failed: {e}")
        sys.exit(1)

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(GTFS_DIR)

    print(f"Extracted to {GTFS_DIR}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update GTFS static data")
    parser.add_argument("--refetch", action="store_true")
    args = parser.parse_args()

    if args.refetch:
        download()

    print("Initializing sqlite db...")
    with sqlite3.connect(DB_PATH) as conn:
        load(conn)
