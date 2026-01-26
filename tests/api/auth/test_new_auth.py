from api.api_manager import ApiManager
from pydantic_ex.pydentic_movie_data import RegisterUserResponse


class TestUser:

    def test_register_user(self, api_manager: ApiManager, creation_user_data):
        response = api_manager.auth_api.register_user(user_data=creation_user_data)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == creation_user_data['email'], "Email не совпадает"

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data).json()

        register_user_response = RegisterUserResponse(**response)
        assert register_user_response.email == creation_user_data['email']
        assert register_user_response.fullName == creation_user_data['fullName']

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()

        RegisterUserResponse(**created_user_response)
        register_user_response_by_id = RegisterUserResponse(
            **super_admin.api.user_api.get_user(created_user_response['id']).json()
        )
        RegisterUserResponse(
            **super_admin.api.user_api.get_user(creation_user_data['email']).json()
        )

        assert register_user_response_by_id.email == creation_user_data['email']
        assert register_user_response_by_id.fullName == creation_user_data['fullName']

    def test_neg_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)
