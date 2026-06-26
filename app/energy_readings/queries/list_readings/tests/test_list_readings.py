import os
from fastapi.testclient import TestClient


def test_list_readings_ok_content_returned(http_client: TestClient):
    response = http_client.get("/readings")
    assert response.status_code == 200
    assert response.json() is not None
    data = response.json()
    assert isinstance(response.json(), list)
    assert len(data) >= 1
    assert data[0].get("id") == 1


