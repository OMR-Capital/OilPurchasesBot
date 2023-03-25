from typing import Optional
from pydantic import BaseModel


class BaseResponse(BaseModel):
    ok: bool
    detail: Optional[str] = None


class SuccessResponse(BaseResponse):
    ok: bool = True


class FailureResponse(BaseResponse):
    ok: bool = False


class BaseRequest(BaseModel):
    pass

