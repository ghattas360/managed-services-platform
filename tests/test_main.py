import pytest
from fastapi.testclient import TestClient

from app.main import app, _items, _next_id


@pytest.fixture(autouse=True)
def clear_items():
    """Reset in-memory store before each test."""
    _items.clear()
    global _next_id
    import app.main as m
    m._next_id = 1
    yield
    _items.clear()
    m._next_id = 1


client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"service": "managed-services-platform", "version": "0.1.0"}


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "timestamp" in body


def test_create_item_returns_201():
    r = client.post("/api/items", json={"name": "widget"})
    assert r.status_code == 201
    body = r.json()
    assert body["name"] == "widget"
    assert "id" in body


def test_list_contains_created_item():
    client.post("/api/items", json={"name": "gadget", "description": "a gadget"})
    r = client.get("/api/items")
    assert r.status_code == 200
    names = [i["name"] for i in r.json()]
    assert "gadget" in names


def test_get_item_404_on_missing():
    r = client.get("/api/items/999")
    assert r.status_code == 404


def test_create_item_422_on_invalid_input():
    r = client.post("/api/items", json={"not_a_name": "oops"})
    assert r.status_code == 422
