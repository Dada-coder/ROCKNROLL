from api.api_manager import ApiManager
import pytest
from constants import REGISTER_ENDPOINT, SUPER_SECRET_DANNIE
from utils.data_generator import DataGenerator

@pytest.fixture
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