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
    """
        Collect movie IDs during test and delete them after test finishes
        """
    movie_ids = []

    yield movie_ids

    logger.info("🧹 Cleanup started: removing created movies")

    for movie_id in movie_ids:
        try:
            resp = authorized_api_manager.movies_api.delete_movies(movie_id)
            logger.info(f"🗑 Deleted movie id={movie_id}, status={resp.status_code}")
            logger.info(f"Delete response status={resp.status_code}, body={resp.text}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to delete movie id={movie_id}, error={e}")

    logger.info("🧹 Cleanup finished")


@pytest.fixture
def updated_data(request):
    data = request.param
    data["price"] = 338
    return data
