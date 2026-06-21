# translink-api

## Running

```bash
uv run uvicorn app:app --reload
# or
make start
```

## Scripts

Add stops to `data/stops.json` by local stop ID:

```bash
uv run scripts/add_stop.py <stop_id> [stop_id2 ...]
```
