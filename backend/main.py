from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Digital Footprint Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev
    allow_credentials=False, # Must be False if origins is "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

from pydantic import BaseModel
from search_logic import deep_dive_search

class SearchRequest(BaseModel):
    name: str
    extra_info: str = ""

import logging
import traceback

# Setup logging if not already done in search_logic, or just add a handler here
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

@app.post("/api/search")
def search_person(request: SearchRequest):
    try:
        logging.info(f"Received search request for: {request.name}")
        results = deep_dive_search(request.name, request.extra_info)
        return {"results": results}
    except Exception as e:
        error_msg = traceback.format_exc()
        logging.error(f"INTERNAL SERVER ERROR: {error_msg}")
        return {"error": "Internal Server Error", "details": str(e)}

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
