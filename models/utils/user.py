from random import choices
from string import ascii_lowercase, digits
from hashlib import blake2s
from typing import Literal

from models import User


def encrypt_access_key(access_key: str) -> str:
    hash_function = blake2s()
    hash_function.update(access_key.encode())
    return hash_function.hexdigest()


async def create_user(name: str, mode: Literal['superuser', 'admin', 'employee']) -> User:
    access_key = ''.join(choices(ascii_lowercase + digits, k=6))

    user = User(
        access_key=encrypt_access_key(access_key)
        name=name,
        mode=mode
    )
    user.save()

