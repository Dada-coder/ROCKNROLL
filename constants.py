import os

BASE_AUTH_URL = "https://auth.dev-cinescope.coconutqa.ru"
BASE_MOVIE_URL = "https://api.dev-cinescope.coconutqa.ru"

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
MOVIES_ENDPOINT = "/movies"

SUPER_SECRET_DANNIE = {
    "email": os.getenv("SUPER_SECRET_DANNIE_1"),
    "password": os.getenv("SUPER_SECRET_DANNIE_2")
}

REQUIRED_FIELDS = {"name", "price", "description", "location"}
