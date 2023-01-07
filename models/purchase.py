from odetam import DetaModel


class Purchase(DetaModel):
    employee_key: str
    supplier: str
    amount: str
    price: str
    card: str
    approved: bool
    approver_id: str
