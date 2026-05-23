import logging
import sys
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
)
logger = logging.getLogger(__name__)

app = FastAPI(title="managed-services-platform", version="0.1.0")

_items: dict[int, dict] = {}
_next_id: int = 1


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None


class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


@app.get("/")
def root():
    logger.info("GET /")
    return {"service": "managed-services-platform", "version": "0.1.0"}


@app.get("/health")
def health():
    logger.info("GET /health")
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/api/items", response_model=list[Item])
def list_items():
    logger.info("GET /api/items count=%d", len(_items))
    return list(_items.values())


@app.post("/api/items", response_model=Item, status_code=201)
def create_item(payload: ItemCreate):
    global _next_id
    item = {"id": _next_id, "name": payload.name, "description": payload.description}
    _items[_next_id] = item
    logger.info("POST /api/items id=%d name=%s", _next_id, payload.name)
    _next_id += 1
    return item


@app.get("/api/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    item = _items.get(item_id)
    if item is None:
        logger.warning("GET /api/items/%d not found", item_id)
        raise HTTPException(status_code=404, detail="Item not found")
    logger.info("GET /api/items/%d", item_id)
    return item
