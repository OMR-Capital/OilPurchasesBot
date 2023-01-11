from odetam import DetaModel


class Chat(DetaModel):
    user: str

    class Config:
        table_name = 'chats'