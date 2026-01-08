class TestMoviesPositive:

    def test_create_movie_pos(self, movie_data, authorized_api_manager, senior_polish):
        resp = authorized_api_manager.movies_api.create_movie(movie_data)
        resp_data = resp.json()
        authorized_api_manager.movies_api.body_check(movie_data, resp_data)

        resp_get = authorized_api_manager.movies_api.get_movie_by_id(movie_id=resp_data['id'])
        resp_get_data = resp_get.json()
        authorized_api_manager.movies_api.body_check(movie_data, resp_get_data)

    def test_create_movie_data_integrity_pos(
        self, movie_data, authorized_api_manager, senior_polish
    ):
        resp = authorized_api_manager.movies_api.create_movie(movie_data)
        resp_data = resp.json()

        for field in ("name", "price", "description", "location", "genreId"):
            assert resp_data[field] == movie_data[field], (f"Поле {field} было изменено сервером")

    # они вовсе не похожи
