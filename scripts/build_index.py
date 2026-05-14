import pickle
import pandas as pd
import os

print("Starting build_index.py")

os.makedirs("data", exist_ok=True)

csv_path = "data/shl_catalog.csv"

if not os.path.exists(csv_path):

    print("ERROR: shl_catalog.csv not found")
    exit()

df = pd.read_csv(csv_path)

df = df.fillna("")

print(f"Loaded {len(df)} rows")

metadata = []

for _, row in df.iterrows():

    item = {
        "name": str(row.get("name", "")),
        "url": str(row.get("url", "")),
        "description": str(row.get("description", "")),
        "duration": str(row.get("duration", "")),
        "remote": str(row.get("remote", "")),
        "adaptive": str(row.get("adaptive", "")),
        "job_levels": str(row.get("job_levels", "")),
        "languages": str(row.get("languages", "")),
        "keys": str(row.get("keys", "")),
        "test_type": str(row.get("test_type", ""))
    }

    metadata.append(item)

output_path = "data/metadata.pkl"

with open(output_path, "wb") as f:

    pickle.dump(metadata, f)

print(f"Saved metadata to {output_path}")
print(f"Total assessments: {len(metadata)}")

