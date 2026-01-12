import pytest


@pytest.mark.parametrize("input_data,expected", [(1, 2), (2, 4), (3, 6)])
def test_multiply_by_two(input_data, expected):
    assert input_data * 2 == expected


@pytest.mark.parametrize(
    "input_minPrice,input_maxPrice,input_genreId", [(100, 300, 3), (110, 350, 1), (120, 400, 2)]
)
def test_multiply_filter(super_admin, senior_polish, input_minPrice, input_maxPrice, input_genreId):
    a = super_admin.api.movies_api.get_movies(
        endpoint=
        f"/movies?minPrice={input_minPrice}&maxPrice={input_maxPrice}&genreId={input_genreId}"
    )


@pytest.mark.parametrize(
    "input_role, expected", [
        ("admin_user", 200),
        ("common_user", 403),
    ], indirect=["input_role"]
)
def test_roles(input_role, expected, created_movie, senior_polish):
    input_role.api.movies_api.delete_movies(created_movie, expected_status=expected)


#nihuase ya pridumal
