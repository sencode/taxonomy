from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI()

from fastapi import FastAPI
 
app = FastAPI()
 
@app.get("/")
def read_root():
    return {"Python": "on Vercel"}