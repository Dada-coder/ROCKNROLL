from custom_requester.custom_requester import CustomRequester
from constants import BASE_MOVIE_URL, MOVIES_ENDPOINT


class MoviesApi(CustomRequester):

    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_MOVIE_URL)

    def create_movie(self, movie_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )

    def get_movies(self, params=None, endpoint=MOVIES_ENDPOINT, expected_status=200):
        return self.send_request(
            method="GET", endpoint=endpoint, params=params, expected_status=expected_status
        )

    def get_movie_by_id(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET", endpoint=f"{MOVIES_ENDPOINT}/{movie_id}", expected_status=expected_status
        )

    def patch_movie(self, patch_data, movie_id=None, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            data=patch_data,
            expected_status=expected_status
        )

    def delete_movies(self, movie_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )
