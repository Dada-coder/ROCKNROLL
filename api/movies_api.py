from custom_requester.custom_requester import CustomRequester
from constants import BASE_MOVIE_URL, REQUIRED_FIELDS


class MoviesApi(CustomRequester):

    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_MOVIE_URL)

    def create_movie(self, movie_data, expected_status=201):
        return self.send_request(
            method="POST", endpoint="/movies", data=movie_data, expected_status=expected_status
        )

    def get_movies(self, params=None, expected_status=200):
        return self.send_request(
            method="GET", endpoint="/movies", params=params, expected_status=expected_status
        )


    def get_movie_by_id(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET", endpoint=f"/movies/{movie_id}", expected_status=expected_status
        )

    def patch_movie(self, patch_data, movie_id=None, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"/movies/{movie_id}",
            data=patch_data,
            expected_status=expected_status
        )

    def delete_movies(self, movie_id, expected_status=200):
        return self.send_request(
            method="DELETE", endpoint=f"/movies/{movie_id}", expected_status=expected_status
        )

    def body_check(self, movie_data, resp_data):
        assert REQUIRED_FIELDS.issubset(resp_data), f"Неполная структура фильма: {resp_data}"
        for item in REQUIRED_FIELDS:
            assert item in movie_data, f"В movie_data отсутствует поле {item}"
            assert resp_data[f"{item}"] == movie_data[f"{item}"], (
                f"Поле {item} отличается, в запросе {movie_data[item]}   "
                f" в ответе {resp_data[item]}"
            )
