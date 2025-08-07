from flask import Flask, jsonify, request
import pickle
import pandas as pd
import plotly.express as px
from supabase import create_client, Client

app = Flask(__name__)

# Load KNN model and pivot
with open("model/knn_model.pkl", "rb") as f:
    model, pivot = pickle.load(f)

# Supabase credentials
SUPABASE_URL = "https://pvefvqwwfvtjnpkzwxjs.supabase.co"
SUPABASE_KEY = ""
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- API Routes ---

@app.route("/")
def home():
    return jsonify({"message": "Recommender API is up"})

@app.route("/recommend/<int:user_id>", methods=["GET"])
def recommend(user_id):
    if user_id not in pivot.index:
        return jsonify({"error": "User not found"}), 404
    user_vector = pivot.loc[[user_id]]
    distances, indices = model.kneighbors(user_vector, n_neighbors=3)
    neighbors = pivot.index[indices.flatten()].tolist()
    return jsonify({"user_id": user_id, "neighbors": neighbors[1:]})  # Skip self

@app.route("/playlists")
def visualize_playlists():
    response = supabase.table("playlists").select("*").execute()
    data = response.data

    if not data:
        return "<h2>No playlists to display</h2>"

    df = pd.DataFrame(data)
    fig = px.bar(df, x="name", y="num_followers", title="Followers per Playlist")
    return fig.to_html(full_html=True)

@app.route("/tracks")
def visualize_tracks():
    response = supabase.table("tracks").select("*").execute()
    data = response.data

    if not data:
        return "<h2>No track data available</h2>"

    df = pd.DataFrame(data)
    df["track_artist"] = df["track_name"] + " — " + df["artist_name"]

    # Get top 10 most common tracks across all playlists
    top_tracks = (
        df["track_artist"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "track_artist"})
        .head(10)
    )

    fig = px.bar(
        top_tracks,
        x="track_artist",
        y="count",
        title="🎧 Top 10 Tracks Across All Playlists",
        labels={"track_artist": "Track — Artist", "count": "Appearances"}
    )
    fig.update_layout(xaxis_tickangle=-45)

    return fig.to_html(full_html=True)
@app.route("/data")
def get_data():
    response = supabase.table("interactions").select("*").execute()
    return jsonify(response.data)

@app.route("/visualize")
def visualize():
    response = supabase.table("interactions").select("*").execute()
    data = response.data
    if not data:
        return "<h2>No data to visualize</h2>"

    df = pd.DataFrame(data)
    fig = px.bar(df, x="user_id", title="Interactions Per User")
    return fig.to_html(full_html=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
