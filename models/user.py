from odetam import DetaModel


class User(DetaModel):
    chat_id: str
    is_admin: bool
    name: str
