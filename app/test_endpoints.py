from django.http import response
from fastapi.testclient import TestClient
from app.main import app


client=TestClient(app)

def test_get_home():
    response=client.get("/") #request to hom,e
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']


def test_home_detail_view():
    response=client.post("/")
    assert response.status_code==200
    assert "application/json" in response.headers['content-type']
    assert response.json() == {"Hello":"Praveen"}
