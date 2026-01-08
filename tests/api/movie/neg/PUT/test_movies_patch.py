import pytest


class TestMoviesNegative:

    @pytest.mark.negative
    def test_patch_movie_unauthorized_neg(
        self, created_movie, unauthorized_api_manager, senior_polish
    ):
        resp = unauthorized_api_manager.movies_api.patch_movie(
            movie_id=created_movie, patch_data={"price": 999}, expected_status=401
        )

    @pytest.mark.negative
    def test_patch_movie_empty_body_neg(self, authorized_api_manager, created_movie, senior_polish):
        authorized_api_manager.movies_api.patch_movie(
            movie_id=created_movie,
            patch_data={"name": None},
            expected_status=404,
        )
