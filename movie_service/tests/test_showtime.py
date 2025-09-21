from datetime import datetime, timedelta

import pytest

@pytest.fixture(scope="module")
def movie_id(client):
    genre_resp = client.post("/genres/", json={"name": "Comedy"})
    genre_id = genre_resp.json()["id"]

    movie_resp = client.post("/movies/", json={
        "title": "Comedy Movie",
        "description": "Funny",
        "poster_image_url": "",
        "duration_minutes": 90,
        "genres": [genre_id]
    })

    movie_id = movie_resp.json()["id"]
    return movie_id

@pytest.fixture(scope="module")
def showtime_id(client, movie_id):
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=100)
    resp = client.post(f"showtime/{movie_id}/", json={
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    })
    assert resp.status_code == 201
    showtime_id = resp.json()["id"]
    return showtime_id

def test_create(client, movie_id):
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=100)
    resp = client.post(f"showtime/{movie_id}/", json={
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    })
    assert resp.status_code == 201


def test_get(client, movie_id):
    resp = client.get(f"/showtime/movie/{movie_id}/")
    assert resp.status_code == 200


def test_update(client, showtime_id):
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=120)
    resp = client.put(f"/showtime/{showtime_id}", json={
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    })
    assert resp.status_code == 200

def test_delete(client, showtime_id):
    resp = client.delete(f"/showtime/{showtime_id}/")
    assert resp.status_code == 204


