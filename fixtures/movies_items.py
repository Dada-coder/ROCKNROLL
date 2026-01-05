import pytest
from utils.data_generator import DataGenerator


@pytest.fixture
def movie_data():
    return DataGenerator.generate_movie_data()


@pytest.fixture
def created_movie(authorized_api_manager, movie_data):
    resp = authorized_api_manager.movies_api.create_movie(movie_data)
    movie_id = resp.json()["id"]

    yield movie_id


    try:
        authorized_api_manager.movies_api.delete_movies(movie_id)
    except ValueError:
        pass