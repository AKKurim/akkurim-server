def _validate_birth_number(birth_number: str) -> bool:
    """
    Validate a birth number.
    """
    birth_number = birth_number.replace("/", "")
    if len(birth_number) != 10 and int(birth_number[:2]) > 54:
        return False

    first_nine = birth_number[:9]
    control_number = birth_number[9]
    mod = int(first_nine) % 11
    if mod == 10:
        mod = 0

    return mod == int(control_number)


def validate_birth_number(birth_number: str) -> str:
    if not _validate_birth_number(birth_number):
        raise ValueError("Invalid birth number")
    return birth_number


def convert_birht_number_to_date(birth_number: str) -> str:
    """
    Convert a birth number to a date.
    """
    year = int(birth_number[:2])
    month = int(birth_number[2:4])
    day = int(birth_number[4:6])

    if year > 54:
        year += 1900
    else:
        year += 2000

    if month > 50:
        month -= 50

    return f"{year}-{month:02d}-{day:02d}"
