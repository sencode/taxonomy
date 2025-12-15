
# api/index.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "runtime": "vercel-python", "framework": "fastapi"}

@app.get("/taxonomies/{name}")
def get_taxonomy(name: str):
    # Example payload; replace with your real logic
    return JSONResponse({"taxonomy": name})
``
