import os

BASE_AUTH_URL = "https://auth.dev-cinescope.coconutqa.ru"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"

SUPER_SECRET_DANNIE = {
    "email": os.getenv("SUPER_SECRET_DANNIE_1"),
    "password": os.getenv("SUPER_SECRET_DANNIE_2")
}

REQUIRED_FIELDS = {"id", "name", "price", "location"}

