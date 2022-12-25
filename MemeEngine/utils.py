from random import choice
from string import ascii_uppercase, digits


def generate_random_string(length: int = 5) -> str:
    """
    Generate a random string of uppercase numbers and digits.

    :param length:  the length of the desired string
    :returns str:   a random string
    """
    return ''.join(choice(ascii_uppercase + digits) for _ in range(length))
