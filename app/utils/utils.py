def validate_birth_number(birth_number: str) -> bool:
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
