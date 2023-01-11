from odetam import DetaModel


class Spread(DetaModel):
    purchase: str
    messages: list[tuple[int, int]]

    class Config:
        table_name = 'spreads'
