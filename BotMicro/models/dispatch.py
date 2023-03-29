from datetime import datetime
from odetam.model import DetaModel


class Dispatch(DetaModel):
    destination: str
    area: str
    amount: float
    creator: str
    create_time: datetime
