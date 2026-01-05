from custom_requester.custom_requester import CustomRequester
from conftest import *
from api.auth_api import *


class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url="https://api.dev-cinescope.coconutqa.ru")


    def create_movie(self, movie_data, expected_status=201):
        resp = self.send_request(
            method="POST",
            endpoint="/movies",
            data=movie_data,
            expected_status=expected_status
        )

        return resp

    def get_movies(self, params=None, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint="/movies",
            params=params,
            expected_status=expected_status
        )

    def get_movie_by_id(self, movie_id=None, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"/movies/{movie_id}",
            expected_status=expected_status
        )



    def patch_movie(self, patch_data, movie_id=None, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"/movies/{movie_id}",
            data=patch_data,
            expected_status=expected_status
        )

    def delete_movies(self,id_movie, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"/movies/{id_movie}",
            expected_status=expected_status
        )