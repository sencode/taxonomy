# api/index.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "framework": "fastapi", "runtime": "vercel-python"}
