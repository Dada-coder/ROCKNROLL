from custom_requester.custom_requester import CustomRequester
from constants import BASE_AUTH_URL


class UserApi(CustomRequester):

    def __init__(self, session):
        self.session = session
        super().__init__(session=session, base_url=BASE_AUTH_URL)

    def get_user(self, user_locator, expected_status=200):
        return self.send_request("GET", f"/user/{user_locator}", expected_status=expected_status)

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST", endpoint="/user", data=user_data, expected_status=expected_status
        )
