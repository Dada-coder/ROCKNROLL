import pytest
from utils.data_generator import DataGenerator
import logging

logger = logging.getLogger("autotests.cleanup")
logger.setLevel(logging.INFO)


@pytest.fixture
def movie_data():

    return DataGenerator.generate_movie_data()


@pytest.fixture
def created_movie(authorized_api_manager, movie_data):
    resp = authorized_api_manager.movies_api.create_movie(movie_data)
    movie_id = resp.json()["id"]

    return movie_id


@pytest.fixture
def senior_polish(authorized_api_manager):
    yield

    logger.info("🧹 Cleanup started: removing test movies")

    resp = authorized_api_manager.movies_api.get_movies()
    movies = resp.json().get("movies", [])

    for movie in movies:
        name = movie.get("name", "")
        movie_id = movie.get("id")

        if name.startswith("Test Movie"):
            logger.info(f"🗑 Deleting movie id={movie_id}, name='{name}'")

            try:
                authorized_api_manager.movies_api.delete_movies(movie_id)
                logger.info(f"✅ Deleted movie id={movie_id}")
            except Exception as e:
                logger.warning(f"⚠️ Failed to delete movie id={movie_id}, error={e}")

    logger.info("🧹 Cleanup finished")


@pytest.fixture
def updated_data(request):
    data = request.param
    data["price"] = 200
    return data
