from datetime import datetime
from odetam import DetaModel


class Fueling(DetaModel):
    employee: str
    time: datetime

    class Config:
        table_name = 'fuelings'
        