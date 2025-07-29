import json
import pandas as pd
from datetime import datetime
from supabase import create_client, Client  

SUPABASE_URL = "https://pvefvqwwfvtjnpkzwxjs.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB2ZWZ2cXd3ZnZ0am5wa3p3eGpzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM1Njk4NjgsImV4cCI6MjA2OTE0NTg2OH0.of6kjPiBOLWMC85eQKPeOkuo0AXzKkE0H4Qlwt7dcuQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load & parse Spotify playlist JSON file
records = []
json_path = r"D:\python\spotify_million_playlist\data\mpd.slice.0-999.json"


with open(json_path, encoding="utf-8") as f:
    data = json.load(f)

records = []
for playlist in data["playlists"]:
    records.append({
        "pid": playlist["pid"],
        "name": playlist["name"],
        "collaborative": playlist["collaborative"].lower() == "true",
        "modified_at": datetime.utcfromtimestamp(playlist["modified_at"]).isoformat(),
        "num_tracks": playlist["num_tracks"],
        "num_albums": playlist["num_albums"],
        "num_followers": playlist["num_followers"]})
    

# Upload data to Supabase in batches
batch_size = 100
for i in range(0, len(records), batch_size):
    batch = records[i:i + batch_size]
    supabase.table("playlists").insert(batch).execute()
    print(f"Uploaded playlists {i} to {i + len(batch) - 1}")