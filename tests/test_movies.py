import pytest
from fastapi.testclient import TestClient

from main import app
from dependencies.auth import API_KEY
from services import movie_service


client = TestClient(app)
AUTH = {"X-API-Key": API_KEY}


@pytest.fixture(autouse=True)
def reset_movies():
    movie_service.movies.clear()
    movie_service.next_id = 1
    yield
    movie_service.movies.clear()
    movie_service.next_id = 1


def valid_movie(**overrides):
    data = {
        "title": "Interstellar",
        "genre": "Sci-Fi",
        "release_year": 2014,
        "rating": 9.0,
        "is_favorite": True,
    }
    data.update(overrides)
    return data


def test_list_movies_empty():
    response = client.get("/api/v1/movies", headers=AUTH)
    assert response.status_code == 200
    assert response.json() == []


def test_create_movie_success():
    response = client.post(
        "/api/v1/movies",
        json=valid_movie(),
        headers=AUTH,
    )
    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Interstellar"


def test_list_movies_contains_created_movie():
    client.post("/api/v1/movies", json=valid_movie(), headers=AUTH)

    response = client.get("/api/v1/movies", headers=AUTH)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_movie_success():
    client.post("/api/v1/movies", json=valid_movie(), headers=AUTH)

    response = client.get("/api/v1/movies/1", headers=AUTH)

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_movie_not_found():
    response = client.get("/api/v1/movies/999", headers=AUTH)
    assert response.status_code == 404


def test_create_movie_blank_title():
    response = client.post(
        "/api/v1/movies",
        json=valid_movie(title="   "),
        headers=AUTH,
    )
    assert response.status_code == 422


def test_create_movie_empty_title():
    response = client.post(
        "/api/v1/movies",
        json=valid_movie(title=""),
        headers=AUTH,
    )
    assert response.status_code == 422


def test_create_movie_rating_below_zero():
    response = client.post(
        "/api/v1/movies",
        json=valid_movie(rating=-1),
        headers=AUTH,
    )
    assert response.status_code == 422


def test_create_movie_rating_above_ten():
    response = client.post(
        "/api/v1/movies",
        json=valid_movie(rating=11),
        headers=AUTH,
    )
    assert response.status_code == 422


def test_create_movie_year_below_limit():
    response = client.post(
        "/api/v1/movies",
        json=valid_movie(release_year=1887),
        headers=AUTH,
    )
    assert response.status_code == 422


def test_create_movie_year_above_limit():
    response = client.post(
        "/api/v1/movies",
        json=valid_movie(release_year=2101),
        headers=AUTH,
    )
    assert response.status_code == 422


def test_update_movie_success():
    client.post("/api/v1/movies", json=valid_movie(), headers=AUTH)

    response = client.put(
        "/api/v1/movies/1",
        json=valid_movie(rating=9.5),
        headers=AUTH,
    )

    assert response.status_code == 200
    assert response.json()["rating"] == 9.5


def test_update_movie_not_found():
    response = client.put(
        "/api/v1/movies/999",
        json=valid_movie(),
        headers=AUTH,
    )
    assert response.status_code == 404


def test_delete_movie_success():
    client.post("/api/v1/movies", json=valid_movie(), headers=AUTH)

    response = client.delete("/api/v1/movies/1", headers=AUTH)

    assert response.status_code == 204
    assert client.get("/api/v1/movies", headers=AUTH).json() == []


def test_delete_movie_not_found():
    response = client.delete("/api/v1/movies/999", headers=AUTH)
    assert response.status_code == 404


def test_request_without_api_key():
    response = client.get("/api/v1/movies")
    assert response.status_code == 401


def test_request_with_wrong_api_key():
    response = client.get(
        "/api/v1/movies",
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 401


def test_request_with_correct_api_key():
    response = client.get("/api/v1/movies", headers=AUTH)
    assert response.status_code == 200
