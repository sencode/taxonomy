from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI()

# Enable CORS so Label Studio can access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Robustly find the JSON file relative to this script
# This handles both local execution and Vercel's unique environment
try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    JSON_PATH = os.path.join(BASE_DIR, 'taxonomies', 'condition-codes.json')
except Exception:
    # Fallback if folder structure is flattened
    JSON_PATH = 'conditions-sample.json'

@app.get("/taxonomy")
def get_taxonomy(path: str = Query(None)):
    """
    Serves the specific condition-codes.json file.
    Label Studio calls this with ?path=PARENT_ID to get nested children.
    """
    
    if not os.path.exists(JSON_PATH):
        print(f"File not found at: {JSON_PATH}")
        raise HTTPException(status_code=404, detail="Taxonomy file not found.")

    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"JSON Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Invalid JSON file.")

    # Label Studio Logic:
    # If path is None, return 'root'. Otherwise return the children of 'path'.
    lookup_key = path if path else "root"
    items = data.get(lookup_key, [])

    return {"items": items}