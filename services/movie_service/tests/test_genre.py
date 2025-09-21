import pytest

def test_create_and_get_genre(client):
    resp = client.post("/genres/", json={"name": "Action"})
    assert resp.status_code == 201


def test_get_all_genre(client):
    resp = client.get("/genres/")
    assert resp.status_code == 200

def test_get_genre_by_name(client):
    resp = client.get("/genres/Action")
    assert resp.status_code == 200
    assert resp.json()['name'] == 'Action'

