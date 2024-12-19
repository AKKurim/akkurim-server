from app.utils.utils import validate_birth_number


def test_validate_birth_number():
    assert validate_birth_number("0409090033") == True
    assert validate_birth_number("0409090034") == False
