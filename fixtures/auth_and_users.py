from api.api_manager import ApiManager
import pytest
import requests
from constants import REGISTER_ENDPOINT, SUPER_SECRET_DANNIE, Roles
from utils.data_generator import DataGenerator
from entities.User import User
from pydantic_ex.pydentic_movie_data import TestUser, RegisterUserResponse


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SUPER_SECRET_DANNIE["email"], SUPER_SECRET_DANNIE["password"], [Roles.SUPER_ADMIN.value],
        new_session
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture
def authorized_api_manager(api_manager):
    api_manager.auth_api.authenticate(SUPER_SECRET_DANNIE)
    return api_manager


@pytest.fixture(scope="session")
def unauthorized_api_manager():
    session = requests.Session()
    return ApiManager(session)


@pytest.fixture
def create_test_user():
    random_password = DataGenerator.generate_random_password()

    user = TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )
    return user.model_dump(mode="json")


@pytest.fixture(scope="function")
def creation_user_data(create_test_user):
    updated_data = create_test_user.copy()
    updated_data.update({"verified": True, "banned": False})
    return updated_data


@pytest.fixture
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST", endpoint=REGISTER_ENDPOINT, data=test_user, expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'], creation_user_data['password'], [Roles.USER.value], new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin = User(
        creation_user_data['email'], creation_user_data['password'], [Roles.ADMIN.value],
        new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    admin.api.auth_api.authenticate(admin.creds)
    return admin


@pytest.fixture
def input_role(request, super_admin, common_user):
    if request.param == "admin_user":
        return super_admin
    if request.param == "common_user":
        return common_user
