import pytest


class TestMoviesNegative:

    @pytest.mark.negative
    def test_delete_movie_not_found_neg(self, authorized_api_manager):
        authorized_api_manager.movies_api.delete_movies(
            movie_id=-1,
            expected_status=404,
        )

    @pytest.mark.negative
    def test_delete_movie_unauthorized_neg(
        self, created_movie, unauthorized_api_manager, senior_polish
    ):
        unauthorized_api_manager.movies_api.delete_movies(
            movie_id=created_movie,
            expected_status=401,
        )
