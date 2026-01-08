from constants import REQUIRED_FIELDS


class TestMoviesPositive:

    def test_get_movies_pos(self, authorized_api_manager, created_movie, senior_polish):
        resp = authorized_api_manager.movies_api.get_movies()
        resp_data = resp.json()
        movies = resp_data["movies"]
        assert movies, "Список фильмов пуст"
        for movie in movies:
            assert REQUIRED_FIELDS.issubset(movie), f"Неполная структура фильма: {movie}"

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

    def test_get_movie_by_id_pos(self, authorized_api_manager, created_movie, senior_polish):
        resp = authorized_api_manager.movies_api.get_movie_by_id(created_movie)
        resp_data = resp.json()

        assert resp_data["id"] == created_movie
