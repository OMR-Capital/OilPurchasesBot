from random import choices
from string import ascii_letters, digits


def awesome_string(length: int = 8):
    return ''.join(choices(ascii_letters + digits, k=length))
