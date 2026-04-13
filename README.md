# LILA BLACK — Player Journey Visualization Tool

A web-based tool for Level Designers to explore player behavior across LILA BLACK's three maps using 5 days of production telemetry data.

**Live URL:** https://lila-black-shobia-s.netlify.app/

---

## Tech Stack

- **Frontend:** Vanilla HTML + JavaScript + Canvas API (no framework)
- **Data Pipeline:** Python (pyarrow + pandas) → JSON
- **Hosting:** Netlify (static site, drag-and-drop deploy)

---

## Setup Steps

### 1. Install Python dependencies
```
pip install pyarrow pandas
```

### 2. Run the data conversion script
```
python convert_data.py
```
This reads all parquet files from the `player_data/` folder and outputs 3 JSON files into `data/`.

### 3. Open locally
Just open `index.html` in your browser. No server needed.

### 4. Deploy
Drag the entire project folder into Netlify. Done.

---

## Folder Structure

```
lila-tool/
├── index.html              ← Full visualization tool (single file)
├── convert_data.py         ← Python script to convert parquet → JSON
├── data/
│   ├── matches.json        ← Match summaries and metadata
│   ├── events.json         ← Combat, loot, storm events with pixel coords
│   └── positions.json      ← Player movement paths (sampled 1-in-5)
├── minimaps/
│   ├── AmbroseValley_Minimap.png
│   ├── GrandRift_Minimap.png
│   └── Lockdown_Minimap.jpg
├── README.md
├── ARCHITECTURE.md
└── INSIGHTS.md
```

---

## Environment Variables

None required. All data is static JSON loaded via fetch().

---

## Features

- Filter by map, date, and match
- Human vs bot path visualization (color coded)
- Kill, death, loot, storm death event markers
- Heatmap overlay for kill zones and traffic
- Timeline playback to watch matches unfold
- Match stats panel (players, kills, loots, storm deaths)
