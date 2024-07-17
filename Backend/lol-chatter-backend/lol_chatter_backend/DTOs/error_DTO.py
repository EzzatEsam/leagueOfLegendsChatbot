from pydantic import BaseModel


class ErrorDTO(BaseModel):
    message: str