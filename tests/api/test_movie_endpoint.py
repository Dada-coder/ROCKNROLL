import pytest
from constants import REQUIRED_FIELDS


class TestMovies:

    def test_create_movie_pos(self, movie_data, authorized_api_manager, senior_polish):
        resp = authorized_api_manager.movies_api.create_movie(movie_data)
        resp_data = resp.json()
        authorized_api_manager.movies_api.body_check(movie_data, resp_data)

        resp_get = authorized_api_manager.movies_api.get_movie_by_id(movie_id=resp_data['id'])
        resp_get_data = resp_get.json()
        authorized_api_manager.movies_api.body_check(movie_data, resp_get_data)

    def test_get_movies_pos(self, authorized_api_manager, created_movie, senior_polish):
        resp = authorized_api_manager.movies_api.get_movies()
        resp_data = resp.json()
        movies = resp_data["movies"]
        assert movies, "Список фильмов пуст"
        for movie in movies:
            assert REQUIRED_FIELDS.issubset(movie), f"Неполная структура фильма: {movie}"

    def test_patch_movie_pos(self, authorized_api_manager, created_movie, senior_polish):
        patch_data = {"price": 999}
        resp_get = authorized_api_manager.movies_api.get_movie_by_id(movie_id=created_movie)
        resp = authorized_api_manager.movies_api.patch_movie(
            movie_id=created_movie, patch_data=patch_data
        )
        assert resp.json()["price"] == patch_data["price"]
        assert resp.json()["price"] != resp_get.json()["price"]
        resp_get = authorized_api_manager.movies_api.get_movie_by_id(created_movie)

    def test_delete_movie_pos(self, authorized_api_manager, created_movie, senior_polish):
        resp = authorized_api_manager.movies_api.delete_movies(created_movie)
        resp_get = authorized_api_manager.movies_api.get_movie_by_id(
            created_movie, expected_status=404
        )

    def test_get_movies_by_price_pos(self, authorized_api_manager):
        price = 200
        resp = authorized_api_manager.movies_api.get_movies(params={"price": price})
        movies = resp.json()["movies"]
        assert movies, "Фильмы по фильтру price не вернулись"

        assert any(movie.get("price") == price for movie in movies), f"Нет фильмов с price={price}"

        assert resp.status_code == 200, (
            f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"
        )

        movies = resp.json()["movies"]
        assert movies, "Фильмы по фильтру price не вернулись"

        assert any(movie.get("price") == price for movie in movies), f"Нет фильмов с price={price}"

    @pytest.mark.negative
    def test_create_movie_invalid_body_neg(self, authorized_api_manager):

        invalid_data = {"name": None}
        resp = authorized_api_manager.movies_api.create_movie(invalid_data, expected_status=400)

    @pytest.mark.negative
    def test_get_movie_not_found_neg(self, authorized_api_manager):
        resp = authorized_api_manager.movies_api.get_movie_by_id(movie_id=-1, expected_status=404)

    @pytest.mark.negative
    def test_patch_movie_unauthorized_neg(self, created_movie, unauthorized_api_manager):

        resp = unauthorized_api_manager.movies_api.patch_movie(
            movie_id=created_movie, patch_data={"price": 999}, expected_status=401
        )

    @pytest.mark.negative
    def test_create_movie_unauthorized_neg(self, movie_data, unauthorized_api_manager):
        resp = unauthorized_api_manager.movies_api.create_movie(movie_data, expected_status=401)
