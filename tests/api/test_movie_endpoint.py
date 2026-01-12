from checkers.movie_response_checker import UtilsCheck
import pytest
from constants import REQUIRED_FIELDS


class TestMovies:

    def test_create_movie_pos(self, movie_data, super_admin, senior_polish):
        resp = super_admin.api.movies_api.create_movie(movie_data)
        resp_data = resp.json()
        UtilsCheck.body_check(movie_data, resp.json())

        resp_get = super_admin.api.movies_api.get_movie_by_id(movie_id=resp_data['id'])
        UtilsCheck.body_check(movie_data, resp_get.json())

    def test_get_movies_pos(self, super_admin, created_movie, senior_polish):
        resp = super_admin.api.movies_api.get_movies()
        resp_data = resp.json()
        movies = resp_data["movies"]
        assert movies, "Список фильмов пуст"
        for movie in movies:
            assert REQUIRED_FIELDS.issubset(movie), f"Неполная структура фильма: {movie}"

    def test_patch_movie_pos(self, super_admin, created_movie, senior_polish):
        patch_data = {"price": 999}
        resp_get = super_admin.api.movies_api.get_movie_by_id(movie_id=created_movie)
        resp = super_admin.api.movies_api.patch_movie(movie_id=created_movie, patch_data=patch_data)
        assert resp.json()["price"] == patch_data["price"]
        assert resp.json()["price"] != resp_get.json()["price"]
        super_admin.api.movies_api.get_movie_by_id(created_movie)

    def test_delete_movie_pos(self, super_admin, created_movie, senior_polish):
        super_admin.api.movies_api.delete_movies(created_movie)
        super_admin.api.movies_api.get_movie_by_id(created_movie, expected_status=404)

    def test_get_movies_by_price_pos(self, super_admin):
        price = 200
        resp = super_admin.api.movies_api.get_movies(params={"price": price})
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
    def test_create_movie_invalid_body_neg(self, super_admin):

        invalid_data = {"name": None}
        super_admin.api.movies_api.create_movie(invalid_data, expected_status=400)

    @pytest.mark.negative
    def test_get_movie_not_found_neg(self, super_admin):
        super_admin.api.movies_api.get_movie_by_id(movie_id=-1, expected_status=404)

    @pytest.mark.negative
    def test_patch_movie_unauthorized_neg(self, created_movie, common_user):

        common_user.api.movies_api.patch_movie(
            movie_id=created_movie, patch_data={"price": 999}, expected_status=403
        )

    @pytest.mark.negative
    def test_create_movie_unauthorized_neg(self, movie_data, common_user):
        common_user.api.movies_api.create_movie(movie_data, expected_status=403)

    @pytest.mark.negative
    def test_common_user_create_movie(self, movie_data, common_user, senior_polish):
        common_user.api.movies_api.create_movie(movie_data, expected_status=403)
