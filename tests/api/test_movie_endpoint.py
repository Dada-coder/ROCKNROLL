import pytest
import requests

from conftest import session
from constants import BASE_AUTH_URL, HEADERS, REGISTER_ENDPOINT,  REQUIRED_FIELDS , SUPER_SECRET_DANNIE
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager

class TestMovies:
    def test_create_movie(self,movie_data, authorized_api_manager):

        resp = authorized_api_manager.movies_api.create_movie(movie_data)
        resp_data = resp.json()
        assert resp.status_code == 201, (f"Expected 201 OK, got {resp.status_code}."
                                             f" "f"Response: {resp.text}")
        assert REQUIRED_FIELDS.issubset(resp_data), f"Неполная структура фильма: {resp_data}"


        resp_get = authorized_api_manager.movies_api.get_movie_by_id(movie_id=resp_data['id'])
        assert resp_get.status_code == 200, (f"Expected 200 OK, got {resp_get.status_code}."
                                             f" "f"Response: {resp_get.text}")

    def test_get_movies(self,created_movie,api_manager: ApiManager):
        resp = api_manager.movies_api.get_movies()
        resp_data = resp.json()
        movies = resp_data["movies"]
        assert resp.status_code == 201 or 200, (f"Expected 201 OK, got {resp.status_code}."
                                                f" "f"Response: {resp.text}")
        assert movies, "Список фильмов пуст"
        for movie in movies:
            assert REQUIRED_FIELDS.issubset(movie), f"Неполная структура фильма: {movie}"

    def test_patch_movie(self,authorized_api_manager, created_movie):
        patch_data = {"price": 999}

        resp = authorized_api_manager.movies_api.patch_movie(
            movie_id=created_movie,
            patch_data=patch_data
        )

        assert resp.status_code == 201 or 200, (f"Expected 201 OK, got {resp.status_code}."
                                                f" "f"Response: {resp.text}")
        assert resp.json()["price"] == patch_data["price"]

        resp_get = authorized_api_manager.movies_api.get_movie_by_id(created_movie)
        assert resp_get.status_code == 200, (f"Expected 200 OK, got {resp_get.status_code}."
                                             f" "f"Response: {resp_get.text}")

    def test_delete_movie(self, authorized_api_manager,created_movie):
        resp = authorized_api_manager.movies_api.delete_movies(created_movie)
        assert resp.status_code == 200, (f"Expected 200 OK, got {resp.status_code}."
                                                f" "f"Response: {resp.text}")

        resp_get = authorized_api_manager.movies_api.get_movie_by_id(created_movie, expected_status=404)
        assert resp_get.status_code == 404, (f"Expected 404 , got {resp_get.status_code}."
                                         f" "f"Response: {resp_get.text}")

    def test_get_movies_by_published(self, authorized_api_manager):
        resp = authorized_api_manager.movies_api.get_movies(
            params={"published": True}
        )

        assert resp.status_code == 200 ,(f"Expected 200 OK, got {resp.status_code}."
                                                f" "f"Response: {resp.text}")

        movies = resp.json()["movies"]
        assert movies, "Фильмы не вернулись"

        assert any(
            movie.get("published") is True
            for movie in movies
        ), "Фильм не вышел"

    @pytest.mark.negative
    def test_create_movie_invalid_body(self, authorized_api_manager):

        invalid_data = {"name": None}

        resp = authorized_api_manager.movies_api.create_movie(
            invalid_data,
            expected_status=400
        )

        assert resp.status_code == 400 ,(f"Expected 400 , got {resp.status_code}."
                                                f" "f"Response: {resp.text}")

    @pytest.mark.negative
    def test_get_movie_not_found(self, api_manager: ApiManager):
        resp = api_manager.movies_api.get_movie_by_id(
            movie_id=-1,
            expected_status=404
        )

        assert resp.status_code == 404 ,(f"Expected 404 , got {resp.status_code}."
                                                f" "f"Response: {resp.text}")

    @pytest.mark.negative
    def test_patch_movie_unauthorized(self,created_movie, unauthorized_api_manager):

        resp = unauthorized_api_manager.movies_api.patch_movie(
            movie_id=created_movie,
            patch_data={"price": 999},
            expected_status=401
        )

        assert resp.status_code == 401 ,(f"Expected 401 , got {resp.status_code}."
                                                f" "f"Response: {resp.text}")

    @pytest.mark.negative
    def test_create_movie_unauthorized(self, movie_data, unauthorized_api_manager):



        resp = unauthorized_api_manager.movies_api.create_movie(
            movie_data,
            expected_status=401
        )

        assert resp.status_code == 401 ,(f"Expected 401, got {resp.status_code}."
                                                f" "f"Response: {resp.text}")

