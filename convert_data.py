import pyarrow.parquet as pq
import pandas as pd
import os
import json

# ============================================================
# CHANGE THIS PATH to where your player_data folder is
# ============================================================
DATA_PATH = r"C:\Users\NIVETHA S\Downloads\player_data\player_data"
OUTPUT_PATH = r"C:\Users\NIVETHA S\Desktop\lila-tool\data"
# ============================================================

MAP_CONFIG = {
    "AmbroseValley": {"scale": 900,  "origin_x": -370, "origin_z": -473},
    "GrandRift":     {"scale": 581,  "origin_x": -290, "origin_z": -290},
    "Lockdown":      {"scale": 1000, "origin_x": -500, "origin_z": -500},
}

def world_to_pixel(x, z, map_id):
    cfg = MAP_CONFIG.get(map_id)
    if not cfg:
        return None, None
    u = (x - cfg["origin_x"]) / cfg["scale"]
    v = (z - cfg["origin_z"]) / cfg["scale"]
    px = round(u * 1024, 2)
    py = round((1 - v) * 1024, 2)
    return px, py

def is_bot(user_id):
    return str(user_id).isdigit()

def load_all_data():
    all_rows = []
    days = ["February_10", "February_11", "February_12", "February_13", "February_14"]
    
    for day in days:
        day_path = os.path.join(DATA_PATH, day)
        if not os.path.exists(day_path):
            print(f"Skipping {day} - folder not found")
            continue
        
        files = os.listdir(day_path)
        print(f"Loading {day}: {len(files)} files...")
        
        for filename in files:
            filepath = os.path.join(day_path, filename)
            try:
                table = pq.read_table(filepath)
                df = table.to_pandas()
                
                # Decode event bytes to string
                df['event'] = df['event'].apply(
                    lambda x: x.decode('utf-8') if isinstance(x, bytes) else str(x)
                )
                
                # Add day column
                df['day'] = day
                
                all_rows.append(df)
            except Exception as e:
                continue
    
    if not all_rows:
        print("ERROR: No data loaded. Check your DATA_PATH!")
        return None
    
    df_all = pd.concat(all_rows, ignore_index=True)
    print(f"Total rows loaded: {len(df_all)}")
    return df_all

def process_and_export(df):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    
    # Add pixel coordinates
    df[['px', 'py']] = df.apply(
        lambda row: pd.Series(world_to_pixel(row['x'], row['z'], row['map_id'])),
        axis=1
    )
    
    # Add is_bot flag
    df['is_bot'] = df['user_id'].apply(is_bot)
    
    # Clean match_id (remove .nakama-0)
    df['match_id_clean'] = df['match_id'].str.replace('.nakama-0', '', regex=False)
    
    # Convert timestamp to ms number for JS
    df['ts_ms'] = pd.to_datetime(df['ts']).astype('int64') // 1_000_000
    
    # ── Export 1: Summary (matches list for dropdowns) ──
    summary = df.groupby(['match_id_clean', 'map_id', 'day']).agg(
        total_events=('event', 'count'),
        human_players=('user_id', lambda x: x[~df.loc[x.index, 'is_bot']].nunique()),
        bot_players=('user_id', lambda x: x[df.loc[x.index, 'is_bot']].nunique()),
    ).reset_index()
    summary.to_json(os.path.join(OUTPUT_PATH, 'matches.json'), orient='records')
    print(f"Exported matches.json ({len(summary)} matches)")
    
    # ── Export 2: Events only (no position spam) ──
    combat_events = ['Kill', 'Killed', 'BotKill', 'BotKilled', 'KilledByStorm', 'Loot']
    df_events = df[df['event'].isin(combat_events)].copy()
    df_events = df_events[['user_id', 'match_id_clean', 'map_id', 'day', 'px', 'py', 'event', 'ts_ms', 'is_bot']]
    df_events = df_events.dropna(subset=['px', 'py'])
    df_events.to_json(os.path.join(OUTPUT_PATH, 'events.json'), orient='records')
    print(f"Exported events.json ({len(df_events)} events)")
    
    # ── Export 3: Positions (sampled - 1 in every 5 for speed) ──
    df_pos = df[df['event'].isin(['Position', 'BotPosition'])].copy()
    df_pos = df_pos.iloc[::5]  # take every 5th row to reduce file size
    df_pos = df_pos[['user_id', 'match_id_clean', 'map_id', 'day', 'px', 'py', 'ts_ms', 'is_bot']]
    df_pos = df_pos.dropna(subset=['px', 'py'])
    df_pos.to_json(os.path.join(OUTPUT_PATH, 'positions.json'), orient='records')
    print(f"Exported positions.json ({len(df_pos)} positions)")
    
    print("\n✅ ALL DONE! Check your lila-tool/data folder.")

# Run it
print("Starting data conversion...")
df = load_all_data()
if df is not None:
    process_and_export(df)
