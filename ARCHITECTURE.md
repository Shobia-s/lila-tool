# Architecture

## What I Built and Why

| Decision | Choice | Reason |
|----------|--------|--------|
| Frontend | Vanilla HTML + Canvas | No build step, instant deploy, full control over rendering |
| Data format | JSON (converted from parquet) | Browser can't read parquet natively; JSON loads with a simple fetch() |
| Hosting | Netlify static | Free, instant, shareable link with drag-and-drop deploy |
| No framework | Plain JS | Faster to ship, no dependencies, easier to debug under time pressure |

---

## How Data Flows

```
Raw parquet files (player_data/)
        ↓
convert_data.py  (Python + pyarrow + pandas)
        ↓  decodes bytes, converts coords, samples positions 1-in-5
        ↓
data/matches.json     → match list for dropdowns + stats panel
data/events.json      → kill / death / loot / storm events with pixel coords
data/positions.json   → movement paths (sampled to keep file size small)
        ↓
index.html loads all 3 via fetch() on page load
        ↓
User selects match → filter by match_id_clean
        ↓
Canvas API draws paths + event markers on top of minimap image
```

---

## Coordinate Mapping — The Tricky Part

Game world uses 3D coordinates (x, y, z). For the 2D minimap:
- `y` = elevation (ignored for 2D plotting)
- `x` and `z` are the horizontal plane coordinates

Each map has a known scale and world origin. The conversion formula:

```
u = (world_x - origin_x) / scale
v = (world_z - origin_z) / scale

pixel_x = u * 1024
pixel_y = (1 - v) * 1024    ← Y is flipped because image origin is top-left
```

Map configs used:

| Map | Scale | Origin X | Origin Z |
|-----|-------|----------|----------|
| AmbroseValley | 900 | -370 | -473 |
| GrandRift | 581 | -290 | -290 |
| Lockdown | 1000 | -500 | -500 |

The canvas is then scaled from 1024px (native) to whatever the image renders at in the browser using a `scale = canvas.width / 1024` multiplier applied at draw time.

---

## Assumptions Made

| Ambiguity | Assumption |
|-----------|------------|
| `event` column stored as bytes | Decoded with `.decode('utf-8')` in Python before export |
| Position events dominate (~85%) | Sampled 1-in-5 positions to keep JSON size manageable without losing path shape |
| Timestamps are match-relative but not zero-based | Normalized to 0 on match load so timeline always starts at 0:00 |
| February 14 is partial | Included as-is, noted in README |
| Bot detection | Numeric user_id = bot, UUID = human (per README spec) |
| `match_id` contains `.nakama-0` suffix | Stripped for display and filtering |

---

## Major Tradeoffs

| Considered | Decided | Why |
|------------|---------|-----|
| React vs Vanilla JS | Vanilla JS | No build step, ships faster |
| Serve parquet directly via DuckDB-WASM | Pre-convert to JSON | Simpler, no WASM overhead, works on any static host |
| Load all data at once vs lazy per match | Load all at once | Data is small enough (~2MB JSON), avoids per-match fetch delay |
| Full positions vs sampled | Sampled 1-in-5 | Reduces positions.json from ~60k to ~15k rows, still shows accurate paths |
| WebGL heatmap vs Canvas 2D | Canvas 2D radial gradients | Sufficient quality, much simpler code |
