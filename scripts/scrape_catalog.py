import requests
import pandas as pd
import json
import os
import re

URL = "https://tcp-us-prod-rnd.shl.com/voiceRater/shl-ai-hiring/shl_product_catalog.json"

os.makedirs("data", exist_ok=True)

print("Downloading catalog...")

response = requests.get(URL, timeout=60)

raw_text = response.text

clean_text = re.sub(
    r'[\x00-\x1F\x7F]',
    '',
    raw_text
)

catalog = json.loads(clean_text)

rows = []

for item in catalog:

    rows.append({
        "name": item.get("name", ""),
        "url": item.get("link", ""),
        "description": item.get("description", ""),
        "duration": item.get("duration", ""),
        "remote": item.get("remote", ""),
        "adaptive": item.get("adaptive", ""),
        "job_levels": ", ".join(item.get("job_levels", [])),
        "languages": ", ".join(item.get("languages", [])),
        "keys": ", ".join(item.get("keys", [])),
        "test_type": ", ".join(item.get("keys", []))
    })

df = pd.DataFrame(rows)

df = df.fillna("")

df.to_csv(
    "data/shl_catalog.csv",
    index=False,
    encoding="utf-8-sig"
)

with open(
    "data/catalog_raw.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(catalog, f, indent=2)

print(f"Saved {len(df)} assessments")

