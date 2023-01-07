from odetam import DetaModel


class Purchase(DetaModel):
    employee_id: int
    supplier: str
    amount: str
    price: str
    card: str
    active: bool
