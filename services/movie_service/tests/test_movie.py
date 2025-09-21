import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

@pytest.fixture
def sample_movie():
    return {
        "title": "Inception",
        "description": "A sci-fi thriller",
        "duration_minutes": 148
    }

def test_create_movie(client: TestClient, sample_movie):
    response = client.post("/movies/", json=sample_movie)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_movie["title"]
    assert "id" in data

def test_get_all_movies(client: TestClient, sample_movie):
    # First create one
    client.post("/movies/", json=sample_movie)

    response = client.get("/movies/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "title" in data[0]

def test_get_movie_by_id(client: TestClient, sample_movie):
    created = client.post("/movies/", json=sample_movie).json()
    movie_id = created["id"]

    response = client.get(f"/movies/{movie_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == movie_id
    assert data["title"] == sample_movie["title"]

def test_get_movie_by_id_not_found(client: TestClient):
    fake_id = str(uuid4())
    response = client.get(f"/movies/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie doesn't exist"

def test_update_movie_by_id(client: TestClient, sample_movie):
    created = client.post("/movies/", json=sample_movie).json()
    movie_id = created["id"]

    update_data = {"title": "Inception Reloaded", "description": "Updated", "duration_minutes": 150}
    response = client.put(f"/movies/{movie_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Inception Reloaded"
    assert data["duration_minutes"] == 150

def test_update_movie_not_found(client: TestClient):
    fake_id = str(uuid4())
    update_data = {"title": "Ghost", "description": "No movie", "duration": 120}
    response = client.put(f"/movies/{fake_id}", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie doesn't exist"

def test_delete_movie_by_id(client: TestClient, sample_movie):
    created = client.post("/movies/", json=sample_movie).json()
    movie_id = created["id"]

    response = client.delete(f"/movies/{movie_id}")
    assert response.status_code == 204

    # Verify it’s gone
    response = client.get(f"/movies/{movie_id}")
    assert response.status_code == 404

def test_delete_movie_not_found(client: TestClient):
    fake_id = str(uuid4())
    response = client.delete(f"/movies/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie doesn't exist"

def test_add_genres(client: TestClient, sample_movie):
    # Create movie
    movie = client.post("/movies/", json=sample_movie).json()
    movie_id = movie["id"]

    # Create a genre (assuming you have /genres API)
    genre = client.post("/genres/", json={"name": "Sci-Fi"}).json()
    genre_id = genre["id"]

    # Add genre to movie
    response = client.patch(f"/movies/{movie_id}", params={"genre_id": genre_id})
    assert response.status_code == 200
    data = response.json()
    assert any(g["id"] == genre_id for g in data["genres"])

def test_add_genres_not_found(client: TestClient):
    fake_movie_id = str(uuid4())
    fake_genre_id = str(uuid4())
    response = client.patch(f"/movies/{fake_movie_id}", params={"genre_id": fake_genre_id})
    assert response.status_code == 404
    assert response.json()["detail"] == "Details doesn't exist"
