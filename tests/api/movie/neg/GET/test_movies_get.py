import pytest


class TestMoviesNegative:

    @pytest.mark.negative
    def test_get_movie_not_found_neg(self, authorized_api_manager):
        resp = authorized_api_manager.movies_api.get_movie_by_id(movie_id=-1, expected_status=404)

    def test_get_movies_ignores_invalid_filter_pos(self, authorized_api_manager, senior_polish):
        resp = authorized_api_manager.movies_api.get_movies(params={"price": {}})
        movies = resp.json()["movies"]

        assert movies, "При некорректном фильтре API не вернул фильмы"