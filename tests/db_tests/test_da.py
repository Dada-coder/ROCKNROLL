from checkers.movie_response_checker import UtilsCheck
import pytest


def test_delete_movie_db(movie_data_for_db, db_helper):
    updated_movie_data = movie_data_for_db
    updated_movie_data["name"] = "Test Movie eshkinkot3"
    movie = db_helper.DB_get_movie_by_name("Test Movie eshkinkot3")
    if movie is None:
        db_helper.DB_create_test_movie(updated_movie_data)
        movie = db_helper.DB_get_movie_by_name("Test Movie eshkinkot3")
        db_helper.DB_delete_movie_by_id(movie.id)
    else:
        movie = db_helper.DB_get_movie_by_name("Test Movie eshkinkot3")
        db_helper.DB_delete_movie_by_id(movie.id)


@pytest.mark.db
def test_create_movie_pos(movie_data_for_db, db_helper):
    updated_movie_data = movie_data_for_db
    updated_movie_data["name"] = "Test Movie eshkinkot"
    assert not db_helper.DB_get_movie_by_name("Test Movie eshkinkot")
    resp = db_helper.DB_create_test_movie(updated_movie_data)
    assert db_helper.DB_get_movie_by_name("Test Movie eshkinkot")
    db_helper.DB_delete_movie_by_id(resp.id)
    assert not db_helper.DB_get_movie_by_name("Test Movie eshkinkot")
