import pytest


class TestMoviesNegative:

    @pytest.mark.negative
    def test_create_movie_invalid_body_neg(self, authorized_api_manager):
        resp = authorized_api_manager.movies_api.create_movie({"name": None}, expected_status=400)
        assert "id" not in resp.json()

    @pytest.mark.negative
    def test_create_movie_unauthorized_neg(self, movie_data, unauthorized_api_manager):
        resp = unauthorized_api_manager.movies_api.create_movie(movie_data, expected_status=401)
        assert "id" not in resp.json()