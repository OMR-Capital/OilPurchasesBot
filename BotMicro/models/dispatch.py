from datetime import datetime
from typing import Optional
from odetam.model import DetaModel


class Dispatch(DetaModel):
    destination: Optional[str] # deprecated
    acquirer: str # Acquirer key
    area: str
    amount: float
    creator: str
    create_time: datetime
