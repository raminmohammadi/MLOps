from pydantic import BaseModel


class DelayedResponse(BaseModel):
    success: bool = False
    delayed: bool
