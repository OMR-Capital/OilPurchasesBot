from datetime import datetime
from odetam import DetaModel


class Fueling(DetaModel):
    employee: str
    time: datetime
    cost: int

    class Config:
        table_name = 'fuelings'
        