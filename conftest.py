from dotenv import load_dotenv
load_dotenv()
from api.api_manager import ApiManager
from faker import Faker
import pytest
import requests
from constants import BASE_AUTH_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT, SUPER_SECRET_DANNIE
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator

faker = Faker()




@pytest.fixture(scope="session")
def authorized_api_manager(api_manager):
    api_manager.auth_api.authenticate(SUPER_SECRET_DANNIE)
    return api_manager

@pytest.fixture(scope="session")
def unauthorized_api_manager():
    import requests
    session = requests.Session()
    return ApiManager(session)

@pytest.fixture(scope="session")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="session")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_AUTH_URL)

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


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