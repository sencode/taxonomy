from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI()

# ---------------------------------------------------------
# 1. CORS Configuration
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 2. Path Resolution
# ---------------------------------------------------------
try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TAXONOMY_DIR = os.path.join(BASE_DIR, 'taxonomies')
except Exception:
    TAXONOMY_DIR = 'taxonomies'

@app.get("/taxonomy/{name}")
def get_taxonomy(name: str, path: str = Query(None)):
    
    # Security check
    if ".." in name or "/" in name or "\\" in name:
        raise HTTPException(status_code=400, detail="Invalid taxonomy name.")

    file_path = os.path.join(TAXONOMY_DIR, f"{name}.json")

    if not os.path.exists(file_path):
        print(f"Error: Could not find file at {file_path}")
        raise HTTPException(status_code=404, detail=f"Taxonomy '{name}' not found.")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    lookup_key = path if path else "root"
    items = data.get(lookup_key, [])
    
    return {"items": items}