
from datetime import datetime
from typing import Optional
from aiogram.types import Message

from models import Fueling, User


async def new_fueling(message: Message, cost: int) -> Optional[Fueling]:
    result = User.query(User.chat_id == message.chat.id)

    if not result:
        return None

    employee = result.pop()

    fueling = Fueling(
        employee=employee.key,
        time=datetime.now(),
        cost=cost
    )
    fueling.save()

    return fueling
