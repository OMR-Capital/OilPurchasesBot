from odetam import DetaModel


class User(DetaModel):
    name: str
    is_admin: bool
