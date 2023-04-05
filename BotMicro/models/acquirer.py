from typing import Optional
from odetam.model import DetaModel
from pydantic import validator

from utils.awesome_random import awesome_string


class Acquirer(DetaModel):
    name: str
    deleted: bool = False
    
    @validator('key', pre=True, always=True)
    def set_key(cls, v: Optional[str]) -> str:
        return v or awesome_string()
    