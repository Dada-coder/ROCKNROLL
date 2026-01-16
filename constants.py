import os
from enum import Enum


class Roles(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


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

GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'