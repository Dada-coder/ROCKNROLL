class TestMoviesPositive:

    def test_patch_movie_pos(self, authorized_api_manager, created_movie, senior_polish):
        patch_data = {"price": 999}
        resp_get = authorized_api_manager.movies_api.get_movie_by_id(movie_id=created_movie)
        resp = authorized_api_manager.movies_api.patch_movie(
            movie_id=created_movie, patch_data=patch_data
        )
        assert resp.json()["price"] == patch_data["price"]
        assert resp.json()["price"] != resp_get.json()["price"]
        resp_get = authorized_api_manager.movies_api.get_movie_by_id(created_movie)

    def test_patch_movie_description_pos(
        self, authorized_api_manager, created_movie, senior_polish
    ):
        patch_data = {"description": "Updated description"}

        resp = authorized_api_manager.movies_api.patch_movie(
            movie_id=created_movie,
            patch_data=patch_data,
        )

        assert resp.json()["description"] == patch_data["description"]
