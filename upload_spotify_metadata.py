import json
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://pvefvqwwfvtjnpkzwxjs.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB2ZWZ2cXd3ZnZ0am5wa3p3eGpzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM1Njk4NjgsImV4cCI6MjA2OTE0NTg2OH0.of6kjPiBOLWMC85eQKPeOkuo0AXzKkE0H4Qlwt7dcuQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

json_path = r"D:\python\spotify_million_playlist\data\mpd.slice.0-999.json"
with open (json_path, encoding="utf-8") as f:
    data = json.load(f)

records = []
for playlist in data["playlists"]:
    pid = playlist["pid"]
    for track in playlist["tracks"]:
        records.append({
            "pid": pid,
            "pos": track["pos"],
            "artist_name": track["artist_name"],
            "track_uri": track["track_uri"],
            "track_name": track["track_name"],
            "album_uri": track["album_uri"],
            "duration_ms": track["duration_ms"],
            "album_name": track["album_name"]
        })

    
# Upload data to Supabase in batches
batch_size = 100
for i in range(0, len(records), batch_size):
    batch = records[i:i + batch_size]
    supabase.table("tracks").insert(batch).execute()
    print(f"Uploaded tracks {i} to {i + len(batch) - 1}")