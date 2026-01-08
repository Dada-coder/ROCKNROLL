class TestMoviesPositive:

    def test_delete_movie_pos(self, authorized_api_manager, created_movie, senior_polish):
        resp = authorized_api_manager.movies_api.delete_movies(created_movie)
        resp_get = authorized_api_manager.movies_api.get_movie_by_id(
            created_movie, expected_status=404
        )

    def test_delete_movie_idempotent_get_pos(
        self, authorized_api_manager, created_movie, senior_polish
    ):
        authorized_api_manager.movies_api.delete_movies(created_movie)

        authorized_api_manager.movies_api.get_movie_by_id(
            movie_id=created_movie, expected_status=404
        )
