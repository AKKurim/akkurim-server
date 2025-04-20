from app.features.athlete.utils import (
    _validate_birth_number,
    convert_birht_number_to_date,
)


def test_validate_birth_number():
    assert _validate_birth_number("0409090033")
    assert not _validate_birth_number("0409090034")


def test_convert_birht_number_to_date():
    assert convert_birht_number_to_date("0409090033") == "2004-09-09"
    assert convert_birht_number_to_date("6459290034") == "1964-09-29"
