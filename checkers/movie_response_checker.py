from constants import REQUIRED_FIELDS


class UtilsCheck:

    @staticmethod
    def body_check(movie_data, resp_data):
        assert REQUIRED_FIELDS.issubset(resp_data), f"Неполная структура фильма: {resp_data}"
        for item in REQUIRED_FIELDS:
            assert item in movie_data, f"В movie_data отсутствует поле {item}"
            assert resp_data[f"{item}"] == movie_data[f"{item}"], (
                f"Поле {item} отличается, в запросе {movie_data[item]}   "
                f" в ответе {resp_data[item]}"
            )
