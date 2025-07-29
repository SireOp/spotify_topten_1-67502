import os
import pickle
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://pvefvqwwfvtjnpkzwxjs.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB2ZWZ2cXd3ZnZ0am5wa3p3eGpzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM1Njk4NjgsImV4cCI6MjA2OTE0NTg2OH0.of6kjPiBOLWMC85eQKPeOkuo0AXzKkE0H4Qlwt7dcuQ"

# Create the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def train_model():
    # Fetch all interaction data
    response = supabase.table("interactions").select("*").execute()
    data = response.data

    if not data:
        raise Exception("No data received from Supabase")

    # Create a pivot table: rows = users, columns = products, values = interaction
    df = pd.DataFrame(data)
    pivot = df.pivot_table(index="user_id", columns="product_id", values="interaction").fillna(0)

    # Train Nearest Neighbors model
    model = NearestNeighbors(metric="cosine", algorithm="brute")
    model.fit(pivot)

    # Save model and pivot table
    os.makedirs("model", exist_ok=True)
    with open("model/knn_model.pkl", "wb") as f:
        pickle.dump((model, pivot), f)

    print("✅ Model trained and saved from Supabase data!")

if __name__ == "__main__":
    train_model()
