from odetam import DetaModel


class User(DetaModel):
    user_id: int
    name: str
    is_admin: bool
