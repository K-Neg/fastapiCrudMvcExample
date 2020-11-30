from fastapi.testclient import TestClient

from src.server.fastApiApp import app

client = TestClient(app)

def test_home():
    response = client.get("/home")
    assert response.status_code == 200
    
def test_sample():
    response = client.get("/sample")
    assert response.json() =={
        "CarSample":{
            "owner": "Mauricio",
            "manufacturer": "Ferrari",
            "year": 2
        }
    }

def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }