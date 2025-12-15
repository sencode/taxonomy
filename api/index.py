from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI()

# ---------------------------------------------------------
# 1. CORS Configuration
# Essential so Label Studio (e.g., localhost:8080) can fetch data 
# from this API (e.g., your-app.vercel.app) without browser errors.
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your Label Studio URL
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 2. Path Resolution
# We need to find the 'taxonomies' folder relative to this file.
# File structure on Vercel:
# /var/task/
#    ├── api/
#    │    └── index.py      <-- We are here (__file__)
#    └── taxonomies/
#         └── snomed.json
# ---------------------------------------------------------
try:
    # Go up one level from 'api' directory to find project root
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TAXONOMY_DIR = os.path.join(BASE_DIR, 'taxonomies')
except Exception as e:
    # Fallback for some local environments
    TAXONOMY_DIR = 'taxonomies'

@app.get("/taxonomy/{name}")
def get_taxonomy(name: str, path: str = Query(None)):
    """
    Fetches children for a specific taxonomy node.
    Usage: GET /taxonomy/snomed?path=12345
    """
    
    # Security: basic prevention of directory traversal attacks
    if ".." in name or "/" in name or "\\" in name:
        raise HTTPException(status_code=400, detail="Invalid taxonomy name.")

    file_path = os.path.join(TAXONOMY_DIR, f"{name}.json")

    # Debugging: check if file exists
    if not os.path.exists(file_path):
        # This print statement will show up in Vercel Function Logs
        print(f"❌ Error: Could not find file at {file_path}")
        if os.path.exists(TAXONOMY_DIR):
             print(f"📂 Contents of {TAXONOMY_DIR}: {os.listdir(TAXONOMY_DIR)}")
        else:
             print(f"📂 Directory {TAXONOMY_DIR} does not exist.")
             
        raise HTTPException(status_code=404, detail=f"Taxonomy '{name}' not found.")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON format in taxonomy file.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Label Studio logic:
    # If 'path' is provided, look up that key. If not, look up 'root'.
    lookup_key = path if path else "root"
    
    items = data.get(lookup_key, [])
    
    return {"items": items}
