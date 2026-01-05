from api.api_manager import ApiManager
import pytest
import requests
from constants import BASE_AUTH_URL
from custom_requester.custom_requester import CustomRequester


@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_AUTH_URL)

@pytest.fixture(scope="session")
def http_session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(http_session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(http_session)