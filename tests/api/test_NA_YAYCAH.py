import pytest
import requests
from constants import BASE_AUTH_URL, HEADERS, REGISTER_ENDPOINT,  REQUIRED_FIELDS , SUPER_FUCN_SECRET_DANNIE
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager

class TestMovies:
    def test_create_movie(self,movie_data, api_manager: ApiManager):
        api_manager.auth_api.authenticate(SUPER_FUCN_SECRET_DANNIE) # я не буду перепрятывать mne len'
        resp = api_manager.movies_api.create_movie(movie_data)
        resp_data = resp.json()

        assert "id" in resp_data, "ID фильма отсутствует в ответе"
        assert REQUIRED_FIELDS.issubset(resp_data), f"Неполная структура фильма: {resp_data}"

    def test_get_movies(self,api_manager: ApiManager):
        resp = api_manager.movies_api.get_movies()
        resp_data = resp.json()
        movies = resp_data["movies"]

        assert movies, "Список фильмов пуст"
        for movie in movies:
            assert REQUIRED_FIELDS.issubset(movie), f"Неполная структура фильма: {movie}"

    def test_patch_movie(self, api_manager: ApiManager, created_movie):
        api_manager.auth_api.authenticate(SUPER_FUCN_SECRET_DANNIE)

        patch_data = {"price": 999}

        resp = api_manager.movies_api.patch_movie(
            movie_id=created_movie,
            patch_data=patch_data
        )

        assert resp.status_code == 200
        assert resp.json()["price"] == patch_data["price"]

    def test_get_movies_filter_by_location(self, api_manager):
        location = "MSK"

        resp = api_manager.movies_api.get_movies(
            params={"location": location}
        )

        movies = resp.json()["movies"]
        assert movies

        assert any(
            movie["location"] == location
            for movie in movies
        ), f"Нет фильмов с location={location} на странице"

    @pytest.mark.negative
    def test_create_movie_invalid_body(self, api_manager: ApiManager):
        api_manager.auth_api.authenticate(SUPER_FUCN_SECRET_DANNIE)

        invalid_data = {"name": ""}

        resp = api_manager.movies_api.create_movie(
            invalid_data,
            expected_status=400
        )

        assert resp.status_code == 400

    @pytest.mark.negative
    def test_get_movie_not_found(self, api_manager: ApiManager):
        resp = api_manager.movies_api.get_movie_by_id(
            movie_id=-1,
            expected_status=404
        )

        assert resp.status_code == 404


    @pytest.mark.negative
    def test_patch_movie_unauthorized(self, api_manager: ApiManager):

        api_manager.session.headers.pop("Authorization", None)

        resp = api_manager.movies_api.patch_movie(
            movie_id=api_manager.movies_api.created_movie_id,
            patch_data={"price": 999},
            expected_status=401
        )

        assert resp.status_code == 401

    @pytest.mark.negative
    def test_create_movie_unauthorized(self, movie_data, api_manager: ApiManager):

        api_manager.movies_api.headers.pop("Authorization", None)

        resp = api_manager.movies_api.create_movie(
            movie_data,
            expected_status=401
        )

        assert resp.status_code == 401

