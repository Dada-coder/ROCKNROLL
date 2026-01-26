from constants import REQUIRED_FIELDS
import pytest
from utils.data_generator import DataGenerator


class TestMoviesPositive:

    def test_get_movies_pos(self, authorized_api_manager, created_movie, senior_polish):
        assert authorized_api_manager.movies_api.get_movie_by_id(created_movie)
        resp = authorized_api_manager.movies_api.get_movies()
        resp_data = resp.json()
        movies = resp_data["movies"]
        assert movies, "Список фильмов пуст"
        for movie in movies:
            assert REQUIRED_FIELDS.issubset(movie), f"Неполная структура фильма: {movie}"

    @pytest.mark.parametrize("updated_data", [DataGenerator.generate_movie_data()], indirect=True)
    def test_get_movies_by_price_pos(self, updated_data, authorized_api_manager):
        authorized_api_manager.movies_api.create_movie(updated_data)
        price = 338
        page = 1
        limit = 10
        found = False
        while True:
            resp = authorized_api_manager.movies_api.get_movies(
                params={
                    "price": price,
                    "page": page,
                    "limit": limit
                }
            )
            assert resp.status_code == 200, (
                f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"
            )
            movies = resp.json().get("movies", [])
            if not movies:
                break
            if any(movie.get("price") == price for movie in movies):
                found = True
                break
            page += 1
        assert found, f"Фильм с price={price} не найден ни на одной странице"

    def test_get_movie_by_id_pos(self, authorized_api_manager, created_movie, senior_polish):
        resp = authorized_api_manager.movies_api.get_movie_by_id(created_movie)
        resp_data = resp.json()

        assert resp_data["id"] == created_movie
