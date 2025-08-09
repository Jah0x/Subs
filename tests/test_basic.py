import asyncio
import httpx
from subscription_server.app.main import app
from fastapi.testclient import TestClient

def test_health():
    client = TestClient(app)
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json().get('status') == 'ok'
