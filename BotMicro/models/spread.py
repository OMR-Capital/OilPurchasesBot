from odetam import DetaModel


class Spread(DetaModel):
    messages: list[tuple[int, int]]

    class Config:
        table_name = 'spreads'
