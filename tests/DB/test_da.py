from checkers.movie_response_checker import UtilsCheck
import pytest


def test_db_requests(super_admin, db_helper, created_test_user):
    assert created_test_user == db_helper.DB_get_user_by_id(created_test_user.id)
    assert db_helper.user_exists_by_email("api1@gmail.com")


@pytest.mark.db
def test_create_movie_pos(movie_data, db_helper, super_admin, senior_polish):
    a = movie_data
    a["name"] = "Test Movie eshkinkot"
    assert not db_helper.DB_get_movie_by_name("Test Movie eshkinkot")
    resp = super_admin.api.movies_api.create_movie(a)
    assert db_helper.DB_get_movie_by_name("Test Movie eshkinkot")
    resp_data = resp.json()
    UtilsCheck.body_check(movie_data, resp.json())

    resp_get = super_admin.api.movies_api.get_movie_by_id(movie_id=resp_data['id'])
    UtilsCheck.body_check(movie_data, resp_get.json())
    senior_polish.append(resp_data['id'])


@pytest.mark.db
def test_get_eshkinkot(db_helper):
    assert not db_helper.DB_get_movie_by_name("Test Movie eshkinkot")
